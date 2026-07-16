#!/usr/bin/env python3
"""Regression tests for the practice content contract."""

from __future__ import annotations

import copy
import importlib.util
import re
import unittest
from pathlib import Path


PRACTICE_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = PRACTICE_ROOT / "scripts" / "build-practice-data.py"
SPEC = importlib.util.spec_from_file_location("build_practice_data", BUILD_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load build-practice-data.py")
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class PracticeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curriculum = BUILD.load_json(PRACTICE_ROOT / "data" / "curriculum.json")
        self.packs = [BUILD.load_json(path) for path in sorted((PRACTICE_ROOT / "data" / "question-packs").glob("*.json"))]
        self.schema = BUILD.load_json(PRACTICE_ROOT / "schemas" / "question-bank.schema.json")

    def validate(self, curriculum: object | None = None, packs: object | None = None) -> list[str]:
        return BUILD.validate(
            copy.deepcopy(self.curriculum if curriculum is None else curriculum),
            copy.deepcopy(self.packs if packs is None else packs),
            copy.deepcopy(self.schema),
        )

    @staticmethod
    def keyword_match(response: str, term: str) -> bool:
        normalized_response = " ".join(response.strip().lower().split())
        normalized_term = " ".join(term.strip().lower().split())
        if not normalized_term:
            return False
        if re.fullmatch(r"[a-z0-9_]+", normalized_term):
            return re.search(rf"(?<![a-z0-9_]){re.escape(normalized_term)}(?![a-z0-9_])", normalized_response) is not None
        return normalized_term in normalized_response

    @staticmethod
    def keyword_score(keyword_groups: list[dict[str, object]], response: str) -> int:
        matched_count = sum(
            any(PracticeContractTests.keyword_match(response, term) for term in group["terms"])
            for group in keyword_groups
        )
        return round((matched_count / len(keyword_groups)) * 100)

    def test_current_sources_satisfy_the_contract(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_missing_learning_paths_is_rejected_before_the_ui_can_initialize(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        del curriculum["learningPaths"]
        self.assertIn("curriculum: learningPaths must be a non-empty array", self.validate(curriculum=curriculum))

    def test_active_topic_with_an_unknown_learning_path_is_rejected(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        next(topic for topic in curriculum["topics"] if topic["status"] == "active")["learningPath"] = "missing-path"
        self.assertTrue(any("active topic has invalid learningPath" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_learning_path_id_is_reported_without_raising(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["learningPaths"][0]["id"] = []
        self.assertTrue(any("learningPath ids must be unique" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_stage_and_topic_ids_are_reported_without_raising(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["stages"][0]["id"] = []
        self.assertTrue(any("stage ids must be unique" in error for error in self.validate(curriculum=curriculum)))

        curriculum = copy.deepcopy(self.curriculum)
        curriculum["topics"][0]["id"] = []
        self.assertTrue(any("topic ids must be unique" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_order_item_id_is_reported_without_raising(self) -> None:
        packs = copy.deepcopy(self.packs)
        order_question = next(question for pack in packs for question in pack["questions"] if question["stage"] == "order")
        order_question["answer"]["items"][0]["id"] = []
        self.assertTrue(any("order item ids and expected must be the same unique set" in error for error in self.validate(packs=packs)))

    def test_malformed_question_prerequisite_is_reported_without_raising(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"][0]["prerequisites"] = [[]]
        self.assertTrue(any("prerequisites must be a string array" in error for error in self.validate(packs=packs)))

    def test_invalid_content_block_is_rejected_before_rendering(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"][0]["prompt"] = [{"type": "unsupported", "content": ""}]
        self.assertTrue(any("prompt block 1 requires type(text/code) and non-empty content" in error for error in self.validate(packs=packs)))

    def test_empty_question_pack_is_rejected(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"] = []
        self.assertTrue(any("questions must be a non-empty array" in error for error in self.validate(packs=packs)))

    def test_management_learning_question_does_not_claim_past_exam_origin(self) -> None:
        management_pack = next(pack for pack in self.packs if pack["packId"] == "management-risk-continuity")
        question = next(question for question in management_pack["questions"] if question["id"] == "business-continuity-terms-05")
        self.assertNotIn("examPrompt", question)
        self.assertFalse(any("/01-rounds/" in ref["path"] for ref in question["sourceRefs"]))

    def test_chapter1_system_security_learning_contract(self) -> None:
        curriculum_paths = {path["id"]: path for path in self.curriculum["learningPaths"]}
        curriculum_topics = {topic["id"]: topic for topic in self.curriculum["topics"]}
        system_pack = next(pack for pack in self.packs if pack["packId"] == "system-security")
        questions = {question["id"]: question for question in system_pack["questions"]}

        self.assertEqual(curriculum_paths["system-security"]["status"], "active")
        self.assertEqual(len(questions), 21)
        self.assertEqual(curriculum_topics["linux-account-access"]["sourceSection"], "1.1.1~1.1.3, 1.2.2")
        self.assertEqual(curriculum_topics["linux-log-service-control"]["prerequisites"], ["linux-account-access"])
        self.assertEqual(curriculum_topics["windows-os-hardening"]["sourceSection"], "1.3.2, 1.4")

        self.assertEqual(questions["linux-account-access-04"]["answer"]["blanks"][0]["accepted"], ["/etc/login.defs"])
        self.assertEqual(questions["linux-account-access-04"]["answer"]["blanks"][1]["accepted"], ["PASS_MIN_LEN"])
        self.assertEqual(questions["linux-account-access-07"]["answer"]["blanks"][0]["accepted"], ["644"])
        self.assertEqual(questions["linux-account-access-07"]["answer"]["blanks"][1]["accepted"], ["755"])
        self.assertEqual(questions["linux-log-service-control-02"]["answer"]["accepted"], ["lastcomm"])
        self.assertEqual(
            [blank["accepted"][0] for blank in questions["linux-log-service-control-08"]["answer"]["blanks"]],
            ["utmp", "wtmp", "acct"],
        )
        self.assertEqual(questions["linux-log-service-control-06"]["answer"]["accepted"], ["/etc/securetty"])
        self.assertEqual(
            [blank["accepted"][0] for blank in questions["linux-log-service-control-05"]["answer"]["blanks"]],
            ["disable", "only_from", "no_access", "access_times", "instances"],
        )
        self.assertEqual([blank["accepted"][0] for blank in questions["windows-os-hardening-03"]["answer"]["blanks"]], ["500 × 1000 × 30", "15000000바이트", "이벤트 뷰어에서 해당 로그 속성의 최대 로그 크기"])
        self.assertIn("500 × 1,000 × 30", questions["windows-os-hardening-03"]["answer"]["blanks"][0]["accepted"])
        self.assertEqual(questions["linux-account-access-09"]["answer"]["accepted"], ["x"])

        blank_recall_ids = [
            "linux-account-access-03", "linux-account-access-06", "linux-account-access-08",
            "linux-log-service-control-01", "linux-log-service-control-07",
            "windows-os-hardening-04",
        ]
        for question_id in blank_recall_ids:
            self.assertEqual(questions[question_id]["stage"], "essay")
            self.assertIn("보기 없이", questions[question_id]["prompt"][0]["content"])
            answer = questions[question_id]["answer"]
            self.assertEqual(
                self.keyword_score(answer["keywordGroups"], " ".join(answer["modelAnswer"])),
                100,
                question_id,
            )

        self.assertLess(self.keyword_score(questions["linux-account-access-03"]["answer"]["keywordGroups"], "auth account password session"), 100)
        self.assertLess(self.keyword_score(questions["linux-account-access-06"]["answer"]["keywordGroups"], "SUID SGID Sticky"), 100)
        self.assertLess(self.keyword_score(questions["linux-account-access-08"]["answer"]["keywordGroups"], "비인가 소유자 최소 권한"), 100)
        self.assertLess(self.keyword_score(questions["linux-log-service-control-01"]["answer"]["keywordGroups"], "wtmp lastb lastlog lastcomm"), 100)
        self.assertLess(self.keyword_score(questions["linux-log-service-control-07"]["answer"]["keywordGroups"], "Telnet SSH SFTP root 직접 로그인 버전"), 100)
        self.assertLess(self.keyword_score(questions["windows-os-hardening-04"]["answer"]["keywordGroups"], "Guest 최소 권한 원격접속 패치"), 100)
        self.assertNotIn("examPrompt", questions["linux-log-service-control-06"])

        self.assertFalse(any("netbios" in question_id or "ipsec" in question_id for question_id in questions))

    def test_chapter2_network_p1_learning_contract(self) -> None:
        curriculum_topics = {topic["id"]: topic for topic in self.curriculum["topics"]}
        network_pack = next(pack for pack in self.packs if pack["packId"] == "network-p1-foundations")
        questions = {question["id"]: question for question in network_pack["questions"]}

        self.assertEqual(len(questions), 20)
        self.assertEqual(curriculum_topics["network-packet-basics"]["sourceSection"], "2.1.2~2.1.5")
        self.assertEqual(curriculum_topics["network-attack-analysis"]["prerequisites"], ["network-packet-basics"])
        self.assertEqual(
            [blank["accepted"][0] for blank in questions["network-packet-basics-02"]["answer"]["blanks"]],
            ["echo request", "echo reply", "destination unreachable", "time exceeded"],
        )
        self.assertTrue({"10.0.0.129~10.0.0.190", "10.0.0.129-10.0.0.190"}.issubset(
            questions["network-packet-basics-01"]["answer"]["blanks"][2]["accepted"]
        ))
        self.assertEqual(
            [blank["accepted"][0] for blank in questions["network-dns-monitoring-01"]["answer"]["blanks"]],
            ["udp 53", "tcp 53", "dns cache", "ttl"],
        )
        self.assertNotIn("examPrompt", questions["network-dns-monitoring-01"])
        self.assertNotIn("network-monitoring-controls-01", questions)
        self.assertEqual(
            questions["network-dns-monitoring-03"]["answer"]["accepted"],
            ["dns cache poisoning", "dns 캐시 포이즈닝"],
        )
        reconstructed_question_ids = [question_id for question_id, question in questions.items() if "examPrompt" in question]
        self.assertEqual(reconstructed_question_ids, ["network-monitoring-controls-03"])
        self.assertEqual(
            [blank["accepted"][0] for blank in questions["network-secure-communications-01"]["answer"]["blanks"]],
            ["서버 인증서", "ecdhe", "대칭 세션키"],
        )

        blank_recall_ids = [
            "network-packet-basics-05", "network-attack-analysis-02",
            "network-attack-analysis-03", "network-monitoring-controls-04",
        ]
        for question_id in blank_recall_ids:
            question = questions[question_id]
            self.assertEqual(question["stage"], "essay")
            self.assertIn("보기 없이", question["prompt"][0]["content"])
            answer = question["answer"]
            self.assertEqual(self.keyword_score(answer["keywordGroups"], " ".join(answer["modelAnswer"])), 100, question_id)

        self.assertLess(
            self.keyword_score(questions["network-attack-analysis-02"]["answer"]["keywordGroups"], "SYN Flooding backlog"),
            100,
        )
        self.assertLess(
            self.keyword_score(questions["network-monitoring-controls-04"]["answer"]["keywordGroups"], "alert tcp sid"),
            100,
        )

    def test_management_answer_variants_and_units_match_the_prompt(self) -> None:
        management_pack = next(pack for pack in self.packs if pack["packId"] == "management-risk-continuity")
        questions = {question["id"]: question for question in management_pack["questions"]}

        self.assertTrue({"물리적 통제, 탐지 통제", "물리적 통제와 탐지 통제"}.issubset(questions["control-classification-03"]["answer"]["accepted"]))
        self.assertTrue({"기술적 통제, 예방 통제", "기술적 통제와 예방 통제"}.issubset(questions["control-classification-04"]["answer"]["accepted"]))
        self.assertTrue({"BCP와 DRP", "BCP/DRP"}.issubset(questions["business-continuity-terms-06"]["answer"]["accepted"]))

        ale_answers = questions["quantitative-risk-02"]["answer"]["blanks"][1]["accepted"]
        annual_effect_answers = questions["quantitative-risk-03"]["answer"]["blanks"][0]["accepted"]
        self.assertIn("2,000만원/년", ale_answers)
        self.assertTrue(all("/년" in answer for answer in ale_answers))
        self.assertTrue(all("/년" in answer for answer in annual_effect_answers))

        recovery_time_answers = questions["recovery-objectives-04"]["answer"]["blanks"][2]["accepted"]
        self.assertNotIn("14:00시", recovery_time_answers)

    def test_chapter5_governance_incident_and_privacy_learning_contract(self) -> None:
        governance_pack = next(pack for pack in self.packs if pack["packId"] == "governance-incident-forensics")
        privacy_pack = next(pack for pack in self.packs if pack["packId"] == "privacy-foundations")
        governance_questions = {question["id"]: question for question in governance_pack["questions"]}
        privacy_questions = {question["id"]: question for question in privacy_pack["questions"]}

        self.assertEqual(len(governance_questions), 17)
        self.assertEqual(len(privacy_questions), 15)

        incident_order = governance_questions["incident-response-01"]["answer"]
        self.assertEqual(incident_order["expected"][-1], "recover")
        self.assertEqual(next(item["label"] for item in incident_order["items"] if item["id"] == "recover"), "복구 및 재발방지")
        self.assertNotIn("해결", [item["label"] for item in incident_order["items"]])

        extended_property_answers = governance_questions["information-protection-objectives-02"]["answer"]["blanks"][0]["accepted"]
        self.assertIn("인증성", extended_property_answers)
        self.assertNotIn("인증", extended_property_answers)

        governance_flow = [governance_questions[f"security-governance-0{index}"] for index in range(1, 4)]
        self.assertEqual([question["stage"] for question in governance_flow], ["cloze", "order", "essay"])
        self.assertEqual([question["prerequisites"] for question in governance_flow], [[], ["security-governance-01"], ["security-governance-02"]])
        policy_answers = governance_questions["security-governance-01"]["answer"]["blanks"]
        self.assertNotIn("정책", policy_answers[0]["accepted"])
        self.assertNotIn("방침", policy_answers[0]["accepted"])

        forensic_answers = governance_questions["digital-forensics-04"]["answer"]["blanks"]
        self.assertEqual(forensic_answers[0]["accepted"], ["Live Forensics", "라이브 포렌식"])
        self.assertEqual(forensic_answers[1]["accepted"], ["Dead Forensics", "데드 포렌식"])

        isms_totals = governance_questions["isms-certification-02"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in isms_totals], ["16", "64", "21", "101"])

        report_deadline = governance_questions["information-communications-law-01"]["answer"]["blanks"][1]["accepted"]
        self.assertIn("24시간", report_deadline)

        pseudonymous_purposes = privacy_questions["pseudonymous-information-01"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in pseudonymous_purposes], ["통계작성", "과학적 연구", "공익적 기록보존"])
        self.assertIn("회수·파기", privacy_questions["pseudonymous-information-02"]["answer"]["blanks"][2]["accepted"])
        consent_items = privacy_questions["privacy-consent-lifecycle-01"]["answer"]["blanks"]
        self.assertNotIn("보관 기간", consent_items[2]["accepted"])
        self.assertNotIn("동의 거부권", consent_items[3]["accepted"])
        privacy_rights = privacy_questions["privacy-consent-lifecycle-04"]["answer"]["blanks"]
        self.assertNotIn("동의 취소 요구권", privacy_rights[3]["accepted"])
        self.assertEqual(privacy_rights[3]["accepted"], ["동의 철회권", "동의철회권"])
        self.assertEqual(privacy_rights[3]["label"], "동의 철회 권리")
        self.assertIn("동의를 철회", privacy_questions["privacy-consent-lifecycle-04"]["prompt"][0]["content"])
        self.assertIn("개인정보 영향평가", privacy_questions["privacy-roles-impact-02"]["answer"]["accepted"])

        pia_considerations = privacy_questions["privacy-roles-impact-03"]["answer"]["modelAnswer"]
        self.assertEqual(len(pia_considerations), 5)
        self.assertIn("개인정보의 제3자 제공 여부를 고려한다.", pia_considerations)
        self.assertIn("민감정보 또는 고유식별정보 처리 여부를 고려한다.", pia_considerations)
        pia_answer = privacy_questions["privacy-roles-impact-03"]["answer"]
        pia_groups = pia_answer["keywordGroups"]
        pia_scale_terms = pia_groups[0]["terms"]
        self.assertNotIn("개인정보", pia_scale_terms)
        self.assertIn("처리하는 개인정보의 수", pia_scale_terms)
        self.assertEqual(
            [group["label"] for group in pia_groups],
            ["처리 규모", "제3자 제공", "권리 침해 위험", "특수정보 처리", "보유기간"],
        )
        self.assertEqual(self.keyword_score(pia_groups, " ".join(pia_considerations)), 100)
        self.assertLess(
            self.keyword_score(pia_groups, "처리하는 개인정보의 수, 제공, 위험, 민감정보, 개인정보 보유기간"),
            100,
        )
        pia_thresholds = privacy_questions["privacy-roles-impact-04"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in pia_thresholds], ["5만", "50만", "100만", "검색체계 등 운용체계"])

        biometric_answer = privacy_questions["biometric-information-protection-01"]["answer"]
        self.assertEqual(len(biometric_answer["modelAnswer"]), 6)
        self.assertEqual(
            [group["label"] for group in biometric_answer["keywordGroups"]],
            [
                "비례성 원칙명", "비례성 내용", "적법성 원칙명", "적법성 내용",
                "목적제한 원칙명", "목적제한 내용", "투명성 원칙명", "투명성 내용",
                "안전성 원칙명", "안전성 내용", "통제권 보장 원칙명", "통제권 보장 내용",
            ],
        )
        self.assertEqual(self.keyword_score(biometric_answer["keywordGroups"], " ".join(biometric_answer["modelAnswer"])), 100)
        self.assertEqual(
            self.keyword_score(biometric_answer["keywordGroups"], "비례성 적법성 목적제한 투명성 안전성 통제권 보장"),
            50,
        )
        self.assertIn("생체인식 보호 6가지 원칙", privacy_questions["biometric-information-protection-01"]["examPrompt"][0]["content"])

    def test_chapter5_privacy_operational_controls_contract(self) -> None:
        curriculum_topics = {topic["id"]: topic for topic in self.curriculum["topics"]}
        privacy_pack = next(pack for pack in self.packs if pack["packId"] == "privacy-operational-controls")
        questions = {question["id"]: question for question in privacy_pack["questions"]}

        self.assertEqual(len(questions), 13)
        self.assertEqual(curriculum_topics["privacy-breach-response"]["sourceSection"], "5.7.7")
        self.assertEqual(curriculum_topics["privacy-safeguards"]["sourceSection"], "5.7.8")
        self.assertEqual(curriculum_topics["video-information-devices"]["sourceSection"], "5.7.9")

        breach_deadlines = questions["privacy-breach-response-01"]["answer"]["blanks"]
        self.assertTrue(all("72시간" in blank["accepted"] for blank in breach_deadlines))
        report_conditions = questions["privacy-breach-response-02"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in report_conditions], ["1천", "민감정보 또는 고유식별정보", "외부의 불법적 접근"])
        self.assertIn("examPrompt", questions["privacy-breach-response-03"])
        self.assertEqual(len(questions["privacy-breach-response-03"]["answer"]["modelAnswer"]), 5)

        access_log_fields = questions["privacy-safeguards-01"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in access_log_fields], ["식별자", "접속일시", "접속지", "처리한 정보주체", "수행업무"])
        self.assertIn("2년", questions["privacy-safeguards-02"]["answer"]["accepted"])
        retention_periods = questions["privacy-safeguards-03"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in retention_periods], ["1", "3"])
        encryption_answers = questions["privacy-safeguards-04"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in encryption_answers], ["일방향 암호화", "암호화", "안전하게 관리"])
        self.assertIn("examPrompt", questions["privacy-safeguards-05"])

        public_cctv_reasons = questions["video-information-devices-02"]["answer"]["blanks"]
        self.assertEqual(questions["video-information-devices-01"]["stage"], "recall")
        self.assertEqual(questions["video-information-devices-01"]["answer"]["type"], "short")
        self.assertIn("설치 장소 및 목적", questions["video-information-devices-01"]["answer"]["accepted"])
        self.assertIn("빈칸 (A)", questions["video-information-devices-01"]["examPrompt"][0]["content"])
        self.assertEqual(len(public_cctv_reasons), 6)
        self.assertEqual(
            public_cctv_reasons[5]["accepted"][0],
            "촬영된 영상정보를 저장하지 아니하는 경우로서 대통령령으로 정하는 경우",
        )
        self.assertTrue(all("대통령령으로 정하는 경우" in answer for answer in public_cctv_reasons[5]["accepted"]))
        self.assertIn("녹음기능 사용", questions["video-information-devices-03"]["answer"]["blanks"][1]["accepted"])
        self.assertIn("examPrompt", questions["video-information-devices-04"])
        self.assertEqual(curriculum_topics["video-information-devices"]["title"], "고정형·이동형 영상정보처리기기")
        self.assertNotIn("examPrompt", questions["video-information-devices-05"])
        self.assertEqual(questions["video-information-devices-05"]["answer"]["accepted"][0], "이동형 영상정보처리기기")
        mobile_prompt = questions["video-information-devices-05"]["prompt"][0]["content"]
        self.assertIn("이동 가능한 물체에 부착·거치", mobile_prompt)
        self.assertIn("촬영·전송", mobile_prompt)

    def test_chapter5_final_management_learning_contract(self) -> None:
        curriculum_topics = {topic["id"]: topic for topic in self.curriculum["topics"]}
        management_pack = next(pack for pack in self.packs if pack["packId"] == "management-risk-continuity")
        questions = {question["id"]: question for question in management_pack["questions"]}

        self.assertEqual(curriculum_topics["asset-governance"]["sourceSection"], "5.1.3, 5.1.4")
        self.assertEqual(curriculum_topics["personnel-physical-security"]["sourceSection"], "5.3.2")
        self.assertEqual(curriculum_topics["continuity-strategy"]["sourceSection"], "5.3.3~5.3.5")
        self.assertEqual(curriculum_topics["biometric-information-protection"]["sourceSection"], "5.7.10")

        risk_lifecycle_answer = questions["risk-lifecycle-01"]["answer"]
        self.assertEqual(questions["risk-lifecycle-01"]["stage"], "essay")
        self.assertEqual(risk_lifecycle_answer["type"], "essay")
        self.assertNotIn("items", risk_lifecycle_answer)
        self.assertNotIn("expected", risk_lifecycle_answer)
        self.assertIn("보기 없이", questions["risk-lifecycle-01"]["prompt"][0]["content"])
        self.assertEqual(
            [group["label"] for group in risk_lifecycle_answer["keywordGroups"]],
            [
                "1단계: 위험관리 전략·계획 수립", "2단계: 위험분석", "3단계: 위험평가",
                "4단계: 보호대책 선정", "5단계: 정보보호계획 수립", "6단계: 보호대책 실행",
            ],
        )
        self.assertEqual(
            self.keyword_score(risk_lifecycle_answer["keywordGroups"], " ".join(risk_lifecycle_answer["modelAnswer"])),
            100,
        )
        self.assertLess(
            self.keyword_score(risk_lifecycle_answer["keywordGroups"], "위험분석 위험평가 보호대책 선정"),
            100,
        )

        self.assertEqual(questions["risk-lifecycle-06"]["answer"]["accepted"][0], "위험관리계획")
        risk_techniques = questions["risk-analysis-approaches-04"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in risk_techniques], ["델파이법", "시나리오법", "순위결정법"])

        document_order = questions["asset-governance-01"]["answer"]
        self.assertEqual(document_order["expected"], ["policy", "standard", "procedure", "record"])
        asset_grouping = questions["asset-governance-02"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in asset_grouping], ["가용성", "그룹핑"])
        self.assertIn("보호 우선순위", questions["asset-governance-03"]["answer"]["accepted"][0])

        physical_answer = questions["personnel-physical-security-02"]["answer"]
        self.assertEqual(len(physical_answer["modelAnswer"]), 3)
        self.assertEqual(self.keyword_score(physical_answer["keywordGroups"], " ".join(physical_answer["modelAnswer"])), 100)
        self.assertEqual(self.keyword_score(physical_answer["keywordGroups"], "제한 기록 기기"), 0)

        bcp_order = questions["continuity-strategy-01"]["answer"]
        self.assertEqual(bcp_order["expected"], ["planning", "bia", "strategy", "plan", "maintenance"])
        recovery_site_order = questions["continuity-strategy-02"]["answer"]
        self.assertEqual(recovery_site_order["expected"], ["mirror", "hot", "warm", "cold"])
        backup_modes = questions["continuity-strategy-03"]["answer"]["blanks"]
        self.assertEqual([blank["accepted"][0] for blank in backup_modes], ["증분", "차등"])
        self.assertNotIn("3-2-1", questions["continuity-strategy-03"]["prompt"][0]["content"])
        self.assertIn("증분 백업은 빠르지만", questions["continuity-strategy-03"]["explanation"][0]["content"])
        self.assertNotIn("증분은 백업은", questions["continuity-strategy-03"]["explanation"][0]["content"])
        self.assertIn("복구시험", questions["continuity-strategy-04"]["answer"]["accepted"])


if __name__ == "__main__":
    unittest.main()
