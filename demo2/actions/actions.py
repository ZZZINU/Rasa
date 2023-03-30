from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_DRAWING_WORDS = ["고양이", "산과 나무"]
ALLOWED_SAVE_CHARACTERISTIC = ["white cat", "blue eyes", "diamond necklace"]
ALLOWED_CHANGE_SKETCH = ["wear a hat", "wear a diamond necklace"]

class ValidateDrawSketchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_draw_sketch_form"

    def validate_drawing_word(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `drawing_word` value."""

        if slot_value not in ALLOWED_DRAWING_WORDS:
            dispatcher.utter_message(text=f"'고양이'와 '산과 나무' 중에 선택할 수 있습니다")
            return {"drawing_word": None}
        dispatcher.utter_message(text=f"{slot_value}를 그림판에 그려주세요!")
        return {"drawing_word": slot_value}

    def validate_save_characteristic(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `save_characteristic` value."""

        if slot_value.lower() not in ALLOWED_SAVE_CHARACTERISTIC:
            dispatcher.utter_message(text=f"다른 특징을 알려주세요!")
            return {"save_characteristic": None}
        dispatcher.utter_message(text=f"그리신 그림에 말씀해주신 특징을 넣어 그림을 완성해볼게요. 잠시만 기다려주세요~")
        return {"save_characteristic": slot_value}



class ValidateChangeSketchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_change_sketch_form"

    def validate_change_sketch(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `change_sketch` value."""

        if slot_value not in ALLOWED_CHANGE_SKETCH:
            dispatcher.utter_message(text=f"'wear a hat' 이나 'wear a diamond necklace'처럼 설명해주세요!")
            return {"change_sketch": None}
        dispatcher.utter_message(text=f"말씀해주신대로 그림을 완성해볼게요. 잠시만 기다려주세요~")
        return {"change_sketch": slot_value}