# https://rasa.com/docs/rasa/custom-graph-components
# https://rasa.com/docs/rasa/policies/#custom-policies
# https://zdatainc.com/custom-rasa-policies/

from rasa.core.policies.policy import Policy
from rasa.engine.recipes.default_recipe import DefaultV1Recipe

# TODO: Correctly register your graph component
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.POLICY_WITHOUT_END_TO_END_SUPPORT], is_trainable=True
)
class MyPolicy(Policy):
    ...