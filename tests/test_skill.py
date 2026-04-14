"""Tests for Design Pattern Flash Cards Alexa skill."""
from unittest.mock import MagicMock
from ask_sdk_model import LaunchRequest, IntentRequest, Intent, Slot

import lambda_function as lf
from data import PATTERNS

GAME_LENGTH = lf.GAME_LENGTH  # 23


def make_hi(request, session_attrs=None):
    hi = MagicMock()
    hi.request_envelope.request = request
    hi.attributes_manager.session_attributes = {} if session_attrs is None else dict(session_attrs)
    rb = MagicMock()
    for m in ("speak", "ask", "set_card", "set_should_end_session"):
        getattr(rb, m).return_value = rb
    hi.response_builder = rb
    return hi


def make_intent(name, slots=None):
    slot_objs = {k: Slot(name=k, value=str(v)) for k, v in (slots or {}).items()}
    return IntentRequest(intent=Intent(name=name, slots=slot_objs))


def game_attrs(current_index=0, score=0):
    """Return session attributes for an in-progress game."""
    indices = list(range(GAME_LENGTH))
    return {
        "indices": indices,
        "current_index": current_index,
        "score": score,
        "last_speech": "some definition speech",
    }


class TestLaunchRequest:
    def test_can_handle(self):
        assert lf.LaunchRequestHandler().can_handle(make_hi(LaunchRequest()))

    def test_starts_game_sets_session_attrs(self):
        hi = make_hi(LaunchRequest())
        lf.LaunchRequestHandler().handle(hi)
        attrs = hi.attributes_manager.session_attributes
        assert "indices" in attrs
        assert len(attrs["indices"]) == GAME_LENGTH
        assert attrs["score"] == 0
        assert attrs["current_index"] == 0

    def test_speaks_welcome_and_first_card(self):
        hi = make_hi(LaunchRequest())
        lf.LaunchRequestHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert "Design Pattern" in speech
        assert "Pattern 1 of" in speech

    def test_keeps_session_open(self):
        hi = make_hi(LaunchRequest())
        lf.LaunchRequestHandler().handle(hi)
        hi.response_builder.ask.assert_called_once()


class TestAnswerIntent:
    def test_can_handle(self):
        assert lf.AnswerIntentHandler().can_handle(
            make_hi(make_intent("AnswerIntent"), session_attrs=game_attrs())
        )

    def test_correct_answer_increments_score(self):
        attrs = game_attrs(current_index=0)
        correct = PATTERNS[attrs["indices"][0]]["answer"]
        hi = make_hi(
            make_intent("AnswerIntent", slots={"Answer": correct}),
            session_attrs=attrs,
        )
        lf.AnswerIntentHandler().handle(hi)
        assert hi.attributes_manager.session_attributes["score"] == 1

    def test_correct_answer_case_insensitive(self):
        attrs = game_attrs(current_index=0)
        correct = PATTERNS[attrs["indices"][0]]["answer"].upper()
        hi = make_hi(
            make_intent("AnswerIntent", slots={"Answer": correct}),
            session_attrs=attrs,
        )
        lf.AnswerIntentHandler().handle(hi)
        assert hi.attributes_manager.session_attributes["score"] == 1

    def test_wrong_answer_reveals_correct(self):
        attrs = game_attrs(current_index=0)
        correct = PATTERNS[attrs["indices"][0]]["answer"]
        hi = make_hi(
            make_intent("AnswerIntent", slots={"Answer": "not the answer"}),
            session_attrs=attrs,
        )
        lf.AnswerIntentHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert "Incorrect" in speech
        assert correct in speech

    def test_wrong_answer_does_not_increment_score(self):
        attrs = game_attrs(current_index=0, score=0)
        hi = make_hi(
            make_intent("AnswerIntent", slots={"Answer": "wrong answer"}),
            session_attrs=attrs,
        )
        lf.AnswerIntentHandler().handle(hi)
        assert hi.attributes_manager.session_attributes["score"] == 0

    def test_last_card_ends_game(self):
        attrs = game_attrs(current_index=GAME_LENGTH - 1, score=10)
        correct = PATTERNS[attrs["indices"][GAME_LENGTH - 1]]["answer"]
        hi = make_hi(
            make_intent("AnswerIntent", slots={"Answer": correct}),
            session_attrs=attrs,
        )
        lf.AnswerIntentHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert "Thanks for playing" in speech
        hi.response_builder.set_should_end_session.assert_called_once_with(True)

    def test_no_game_in_progress_starts_game(self):
        hi = make_hi(make_intent("AnswerIntent", slots={"Answer": "factory"}))
        lf.AnswerIntentHandler().handle(hi)
        assert "indices" in hi.attributes_manager.session_attributes


class TestDontKnowIntent:
    def test_can_handle(self):
        assert lf.DontKnowIntentHandler().can_handle(make_hi(make_intent("DontKnowIntent")))

    def test_reveals_correct_answer(self):
        attrs = game_attrs(current_index=0)
        correct = PATTERNS[attrs["indices"][0]]["answer"]
        hi = make_hi(make_intent("DontKnowIntent"), session_attrs=attrs)
        lf.DontKnowIntentHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert correct in speech


class TestRepeatIntent:
    def test_can_handle(self):
        assert lf.RepeatIntentHandler().can_handle(make_hi(make_intent("AMAZON.RepeatIntent")))

    def test_repeats_last_speech(self):
        attrs = game_attrs()
        attrs["last_speech"] = "this is the definition"
        hi = make_hi(make_intent("AMAZON.RepeatIntent"), session_attrs=attrs)
        lf.RepeatIntentHandler().handle(hi)
        speech = hi.response_builder.speak.call_args[0][0]
        assert speech == "this is the definition"


class TestPatternBank:
    def test_has_all_gof_patterns(self):
        assert len(PATTERNS) == 23

    def test_each_pattern_has_answer_and_definition(self):
        for p in PATTERNS:
            assert "answer" in p
            assert "definition" in p
            assert isinstance(p["answer"], str)
            assert isinstance(p["definition"], str)
