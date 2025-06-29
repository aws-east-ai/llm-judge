import os
import re

from litellm import completion
import os

def model_call(model_id, prompt) -> str:
    response = completion(
        model=model_id,
        max_tokens=1024*8,
        messages=[{ "content": prompt,"role": "user"}]
    )
    return response["choices"][0]["message"]["content"]

def llm_eval(story, context):

    prompt = f"""
        Story:
        {story}

        ---

        For these categories, rate the story above on a scale 0-10. Assign rating 0 (worst) to 10 (best). Just output this rating. You are a very harsh literary critic because this story should be excellent since it's for publishing. There should be no weaknesses.

        1. Character Development & Motivation
        When assessing the character's portrayal, look for:
        - How well does the assigned attribute shape the character's personality or actions?
        - Is the character's motivation clear and consistent with their assigned traits?
        - Does the character's reaction to the assigned object or concept reveal something about them?
        - Are their actions aligned with their established motivation?
        - How does the character's personality influence their use of the assigned method?

        2. Plot Structure & Coherence
        When analyzing the story's construction, examine:
        - How effectively does the assigned action drive the plot forward?
        - Does the method of accomplishing the action make sense within the story?
        - Is there a clear connection between the beginning and end despite the 400-word constraint?
        - How well does the assigned concept shape or influence the plot's direction?
        - Are cause and effect relationships clear and logical within the story's framework?

        3. World & Atmosphere
        When evaluating the story's setting and mood, consider:
        - How well do the assigned setting and timeframe work together?
        - Does the tone complement or intentionally contrast with the concept?
        - How effectively does the author use the setting to enhance the action or method?
        - Are the object and setting meaningfully connected?
        - Does the atmosphere support the character's motivation and the story's concept?

        4. Storytelling Impact & Craft
        When evaluating the overall storytelling effectiveness, consider:
        - Does the story evoke an emotional response or make the reader think?
        - Is there effective use of literary devices (metaphor, imagery, symbolism, etc.)?
        - How memorable or unique is the story's perspective or approach?
        - Is there subtext or deeper meaning beyond the surface narrative?
        - Does the ending feel satisfying or purposeful?
        - How well does the writer control pacing and tension?
        - Is the dialogue (if any) natural and purposeful?
        - Does the writing style enhance the story's impact?

        5. Authenticity & Originality
        Checking for signs of formulaic writing, examine:
        - Are there repetitive or unnecessarily flowery phrases that feel machine-like?
        - Does the story rely on common tropes or clichés without subverting them?
        - Is there inconsistent or generic sensory detail?
        - Does the writing feel overly formal or use unnecessarily complex vocabulary?
        - Are there sudden narrative jumps or inconsistencies typical of AI writing?
        - Is character reasoning overly logical without human nuance?
        - Does the story feel like it's following a predictable template?
        - Are metaphors and similes fresh and specific, or generic and overused?
        - Is there nuanced handling of emotion, or just stated feelings?
        - Does the writing show individual style, or could it be from any source?

        6. General score
        Consider:
        - Does the story feel cohesive despite having to incorporate many assigned elements?
        - Are the elements used in service of the story rather than the story being built around them?
        - Does the brief length feel like a deliberate choice rather than a limitation?
        - Is there evidence of creative thinking in how elements are combined and utilized?

        7. The story was supposed to use certain elements. Rate each of them on a 0–10 scale of how tightly it fits into the story's logic, tone, and momentum. Consider how each element shapes the narrative arc, enriches the setting, deepens character motives, and supports the theme. If the story would be less cohesive or compelling without that specific element, give it a higher rating. If using this particular element feels forced and another element in the category would fit better, give it a lower rating. All elements must flow and fit together very well.

        Rating scale:
        0 if it isn't used at all.
        1 if it's jarring or drags the story down.
        10 if removing or swapping it for a similar element would ruin the story's tension, originality, or emotional impact.
        (use any integer number 0 to 10, not just these, and make a precise evalation).

        7 A. Character: {context['vars']['character']}

        7 B. Object: {context['vars']['object']}

        7 C. Core Concept: {context['vars']['core_concept']}

        7 D. Attribute: {context['vars']['attribute']}

        7 E. Action: {context['vars']['action']}

        7 F. Method: {context['vars']['method']}

        7 G. Setting: {context['vars']['setting']}

        7 H. Timeframe: {context['vars']['timeframe']}

        7 I. Motivation: {context['vars']['motivation']}

        7 J. Tone: {context['vars']['tone']}

        Sample output format, you must follow this format and use tags <question></question><grade></grade>:

        <question>1</question><grade>4</grade>
        <question>2</question><grade>7</grade>
        <question>3</question><grade>0</grade>
        <question>4</question><grade>10</grade>
        <question>5</question><grade>9</grade>
        <question>6</question><grade>4</grade>
        <question>7 A</question><grade>2</grade>
        <question>7 B</question><grade>8</grade>
        <question>7 C</question><grade>1</grade>
        <question>7 D</question><grade>4</grade>
        <question>7 E</question><grade>10</grade>
        <question>7 F</question><grade>0</grade>
        <question>7 G</question><grade>0</grade>
        <question>7 H</question><grade>5</grade>
        <question>7 I</question><grade>7</grade>
        <question>7 J</question><grade>2</grade>

        You may not output any extra comments besides these scores.
    """
    
    response = model_call(
        model_id="bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        prompt=prompt
    )
    
    grades = re.findall(r"<grade>(\d+)</grade>", response)
    grades = list(map(int, grades))

    if grades:
        average = sum(grades) / len(grades)
        print("Average grade:", average)
    else:
        print("No grades found.")
    return average, response

def get_assert(output: str, context):
    score, evaluation = llm_eval(output, context)
    return {
        "pass": True,
        "score": score,
        "reason": evaluation,
    }
    