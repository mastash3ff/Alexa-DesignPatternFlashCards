import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from data import PATTERNS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CARD_TITLE = "Design Pattern Flash Cards"
GAME_LENGTH = len(PATTERNS)  # 23


def _build_question_speech(handler_input: HandlerInput) -> str:
    attrs = handler_input.attributes_manager.session_attributes
    pos = attrs["current_index"]
    idx = attrs["indices"][pos]
    definition = PATTERNS[idx]["definition"]
    card_num = pos + 1
    return f"Pattern {card_num} of {GAME_LENGTH}. {definition}"


def _start_game(handler_input: HandlerInput) -> str:
    indices = list(range(GAME_LENGTH))
    random.shuffle(indices)
    attrs = handler_input.attributes_manager.session_attributes
    attrs["indices"] = indices
    attrs["current_index"] = 0
    attrs["score"] = 0
    speech = "Welcome to Design Pattern Flash Cards. I'll read you the GoF pattern definition; say the pattern name. Let's begin. "
    question = _build_question_speech(handler_input)
    attrs["last_speech"] = question
    return speech + question


def _advance_or_end(handler_input: HandlerInput, result_speech: str) -> Response:
    attrs = handler_input.attributes_manager.session_attributes
    current_index = attrs["current_index"]

    if current_index >= GAME_LENGTH - 1:
        score = attrs["score"]
        speech = (
            f"{result_speech} "
            f"You got {score} out of {GAME_LENGTH} correct. "
            "Thanks for playing Design Pattern Flash Cards!"
        )
        return (
            handler_input.response_builder
            .speak(speech)
            .set_card(SimpleCard(CARD_TITLE, speech))
            .set_should_end_session(True)
            .response
        )

    attrs["current_index"] = current_index + 1
    question = _build_question_speech(handler_input)
    attrs["last_speech"] = question
    speech = f"{result_speech} {question}"
    return (
        handler_input.response_builder
        .speak(speech)
        .ask(question)
        .set_card(SimpleCard(CARD_TITLE, speech))
        .response
    )


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = _start_game(handler_input)
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(handler_input.attributes_manager.session_attributes["last_speech"])
            .set_card(SimpleCard(CARD_TITLE, speech))
            .response
        )


class StartOverIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = _start_game(handler_input)
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(handler_input.attributes_manager.session_attributes["last_speech"])
            .set_card(SimpleCard(CARD_TITLE, speech))
            .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        attrs = handler_input.attributes_manager.session_attributes
        if "indices" not in attrs:
            speech = _start_game(handler_input)
            return (
                handler_input.response_builder
                .speak(speech)
                .ask(attrs["last_speech"])
                .response
            )

        slots = handler_input.request_envelope.request.intent.slots
        user_answer = (slots.get("Answer") and slots["Answer"].value) or ""
        user_answer = user_answer.lower().strip()

        idx = attrs["indices"][attrs["current_index"]]
        correct = PATTERNS[idx]["answer"].lower()

        if user_answer == correct:
            attrs["score"] += 1
            result = "Correct!"
        else:
            result = f"Incorrect. The answer was {PATTERNS[idx]['answer']}."

        return _advance_or_end(handler_input, result)


class DontKnowIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DontKnowIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        attrs = handler_input.attributes_manager.session_attributes
        if "indices" not in attrs:
            speech = _start_game(handler_input)
            return (
                handler_input.response_builder
                .speak(speech)
                .ask(attrs["last_speech"])
                .response
            )

        idx = attrs["indices"][attrs["current_index"]]
        result = f"The answer was {PATTERNS[idx]['answer']}."
        return _advance_or_end(handler_input, result)


class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        attrs = handler_input.attributes_manager.session_attributes
        last = attrs.get("last_speech", "")
        if not last:
            speech = _start_game(handler_input)
            return (
                handler_input.response_builder
                .speak(speech)
                .ask(attrs["last_speech"])
                .response
            )
        return (
            handler_input.response_builder
            .speak(last)
            .ask(last)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = (
            "I'll read you a GoF design pattern definition and you say the pattern name. "
            "For example, say 'abstract factory'. "
            "Say 'repeat' to hear the current definition again, "
            "or 'start over' to restart the game. "
            "Would you like to continue?"
        )
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(speech)
            .set_card(SimpleCard(CARD_TITLE, speech))
            .response
        )


class StopCancelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (
            is_intent_name("AMAZON.StopIntent")(handler_input)
            or is_intent_name("AMAZON.CancelIntent")(handler_input)
        )

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = f"Thanks for playing {CARD_TITLE}!"
        return (
            handler_input.response_builder
            .speak(speech)
            .set_should_end_session(True)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("Session ended: %s", handler_input.request_envelope.request.reason)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error("Unhandled exception: %s", exception, exc_info=True)
        speech = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(speech)
            .response
        )


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartOverIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(DontKnowIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(StopCancelIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
