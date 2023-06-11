# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

####################


from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet, ReminderScheduled, ReminderCancelled
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import datetime

# for diffusion
from diffuser.draw import Draw
from diffuser.inpaint import Inpaint
# for checking time, https://blockdmask.tistory.com/549
# import math
# import time

ALLOWED_DRAWING_OBJECTS = [
    "고양이", "산과 나무"
]

ALLOWED_DRAWING_PROMPTS_CAT = [
    "black cat", "white cat", 
    "blue eyes", "yellow eyes", 
    "pearl necklace", "diamonds necklace"
]

ALLOWED_DRAWING_PROMPTS_FOREST = [
    "spring", "summer", "fall", "winter",
]

ALLOWED_INPAINTING_PROMPTS_CAT = [
    "wear a hat", "wear a diamond necklace",
]

ALLOWED_INPAINTING_PROMPTS_FOREST = [
    "bluming flowers",
]


# Validate 'drawing_object' & 'drawing_prompt' slot value
class ValidateDrawingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_drawing_form"

    def validate_drawing_object(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `drawing_object` value."""

        # start = time.time()
        
        if slot_value.lower() not in ALLOWED_DRAWING_OBJECTS:
            dispatcher.utter_message(text=f"'고양이'와 '산과 나무'만 선택하실 수 있어요.")
            return {"drawing_object": None}
        dispatcher.utter_message(text=f"그림판에 {slot_value}를 그려주세요!")

        # end = time.time()
        # print(f"'drawing_object' validation time: {end - start: .10f} sec")

        return {"drawing_object": slot_value}

    def validate_drawing_prompt(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `drawing_prompt` value."""

        # https://stackoverflow.com/questions/59199338/rasa-getting-slot-value-for-use-in-custom-action 해결 방법 링크
        current_drawing_object_value = tracker.get_slot('drawing_object')
        if current_drawing_object_value == "고양이":
            ALLOWED_DRAWING_PROMPTS = ALLOWED_DRAWING_PROMPTS_CAT
        else:
            ALLOWED_DRAWING_PROMPTS = ALLOWED_DRAWING_PROMPTS_FOREST

        for word in slot_value:
            if word.lower().rstrip(',') not in ALLOWED_DRAWING_PROMPTS: ## .lower() 동작하는지 보기
                msg = "죄송하지만 저는 그것을 그릴 수 없어요:( "
                msg += f"제가 그릴 수 있는 {'/'.join(ALLOWED_DRAWING_PROMPTS)} 중에 선택해주세요."
                dispatcher.utter_message(msg)
                return {"drawing_prompt": None}
        # dispatcher.utter_message(text=f"그리신 그림에 말씀해주신 특징을 넣어 그림을 완성해볼게요. 잠시만 기다려주세요~") # domain 에서 똑같이 action하는 답변 있음

        # dispatcher.utter_message(text=f"완성된 {current_drawing_object_value} 그림이에요. 더 수정해보시겠어요?")

        return {"drawing_prompt": slot_value}
    

# Validate 'inpainting_prompt' slot value
class ValidateInpaintingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_inpainting_form"

    def validate_inpainting_prompt(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `inpainting_prompt` value."""

        current_drawing_object_value = tracker.get_slot('drawing_object')
        if current_drawing_object_value == "고양이":
            ALLOWED_INPAINTING_PROMPTS = ALLOWED_INPAINTING_PROMPTS_CAT
        else:
            ALLOWED_INPAINTING_PROMPTS = ALLOWED_INPAINTING_PROMPTS_FOREST

        for word in slot_value:
            if word.lower().rstrip(',') not in ALLOWED_INPAINTING_PROMPTS:
                msg = "죄송하지만 저는 그것을 추가할 수 없어요:( "
                msg += f"제가 추가할 수 있는 {'/'.join(ALLOWED_INPAINTING_PROMPTS)} 중에 선택해주세요."
                dispatcher.utter_message(msg)
                return {"inpainting_prompt": None}
        # dispatcher.utter_message(text=f"그리신 그림에 말씀해주신 특징을 넣어 그림을 완성해볼게요. 잠시만 기다려주세요~") # domain 에서 똑같이 action하는 답변 있음
        
        # if current_drawing_object_value == "고양이":
        #     dispatcher.utter_message(text=f"저는 목걸이나 모자를 씌우게 할 수 있어요! 이 중 추가하고 싶은 부분을 꼼꼼하게 칠해주세요.")
        # else:
        #     dispatcher.utter_message(text=f"저는 나무, 꽃 태양, 구름을 더 그릴 수 있어요! 수정하고 싶은 부분을 꼼꼼하게 칠해주세요.")

        return {"inpainting_prompt": slot_value}


# Submit Drawing Form to Diffuser
class SubmitDrawingForm(Action):
    def name(self) -> Text:
        return "submit_drawing_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit `drawing_form` value."""

        current_drawing_object_value = tracker.get_slot('drawing_object')
        current_drawing_prompt_value = tracker.get_slot('drawing_prompt')

        diffusion = Draw(current_drawing_object_value, current_drawing_prompt_value)
        diffusion.draw_image()

        # 완성된 그림을 다시 받아서 출력하고 (다 그렸다는 message 출력해야함)
        dispatcher.utter_message(text=f"그리신 {current_drawing_object_value} 그림에 말씀해주신 특징을 넣어 그림을 완성했어요! 특징을 더 추가해보시겠어요?")

        return []


# Submit Inpainting Form to Diffuser
class SubmitInpaintingForm(Action):
    def name(self) -> Text:
        return "submit_inpainting_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit `inpainting_form` value."""

        current_inpainting_prompt_value = tracker.get_slot('inpainting_prompt')

        diffusion = Inpaint(current_inpainting_prompt_value)
        diffusion.inpaint_image()

        # 완성된 그림을 다시 받아서 출력하고 (다 그렸다는 message 출력해야함)
        dispatcher.utter_message(text=f"말씀해주신대로 완성된 {tracker.get_slot('drawing_object')} 그림을 완성해봤어요. 마음에 드셨으면 좋겠네요:)")

        # 모든 slot value 초기화, https://forum.rasa.com/t/reset-slot-after-the-forms-complete/35355/2
        return [SlotSet("drawing_object", None), 
                SlotSet("drawing_prompt", None),
                SlotSet("inpainting_prompt", None)]
    

# Response to 'drawing_object' slot value
class ResponseToDrawingObject(Action):
    def name(self) -> Text:
        return "utter_inpaint"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Response to `drawing_object` value."""

        current_drawing_object_value = tracker.get_slot('drawing_object')

        if current_drawing_object_value == "고양이":
            dispatcher.utter_message(text=f"저는 목걸이나 모자를 씌우게 할 수 있어요!")
        else:
            dispatcher.utter_message(text=f"저는 나무, 꽃 태양, 구름을 더 그릴 수 있어요!")

        return []
    
# (추가) 사용자의 응답 없을 때
class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("(알림 설정)")

        date = datetime.datetime.now() + datetime.timedelta(seconds=30)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]

# (추가) 사용자의 응답 없을 때
class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # name = next(tracker.get_slot("PERSON"), "someone")
        dispatcher.utter_message(f"다 칠하셨나요?")

        return []
    

# (추가) 알림 취소 기능 (일정 시간 내에 사용자가 응답을 했을 때)
class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(f"(알림 취소)")

        # Cancel all reminders
        return [ReminderCancelled()]
    
    
#(추가)form slot 리셋  - 다시 그리기 기능  
class ResetFormAction(Action):
    def name(self):
        return "action_reset_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(f"(form reset)")
        # return [SlotSet(slot, None) for slot in tracker.slots.keys()]
        return [SlotSet("drawing_object", None), 
                SlotSet("drawing_prompt", None),
                SlotSet("inpainting_prompt", None)]