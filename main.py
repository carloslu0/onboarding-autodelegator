#Import main libraries
import os
import time
import streamlit as st
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

#Environment variables
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# If dotenv doesn't work, adding this code in to access the API key via the secrets folder in Streamlit
# Set API Keys
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]

# Functions
def process_transcript(prompt_type):
    anthropic = Anthropic()
    selected_prompt = ""
    if prompt_type == 'instruction':
        selected_prompt = instruction_prompt
    elif prompt_type == 'evaluate':
        selected_prompt = evaluate_prompt
    else:
        raise ValueError("Invalid prompt_type. Expected 'instruction' or 'evaluate'")
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=50000,
        temperature=0.5,
        top_k=1.0,
        prompt=f"{HUMAN_PROMPT} {selected_prompt} {AI_PROMPT}",
    )
    return(completion.completion)

def delegation_areas(prompt):
    anthropic = Anthropic()
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=50000,
        temperature=0.5,
        top_k=1.0,
        prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}"
    )
    return(completion.completion)


# Start Streamlit
# Set the Streamlit page configuration
st.set_page_config(page_title="Onboarding Call Autodelegator", page_icon="📁", layout="wide")

# Start Top Information
st.title("Onboarding Call Autodelegator")
st.markdown("##### Get your Client-XP relationship off to a flying start by using this micro-app to generate personalized delegation ideas from the onboarding call")

# End Top Information

# Body
client = st.text_input("What's the name of your client?")
uploaded_file = st.file_uploader("Upload a transcript")

# Add a button
button_pressed = st.button("Process Transcript")

# Execute this block if the button is pressed
if button_pressed:
    if uploaded_file is not None:
        # Read the uploaded file into a string 
        bytes_data = uploaded_file.getvalue()
        st.write("Uploading File....")

        # Call the function to process the transcript  
        transcript = bytes_data.decode()

        # Prompt to extract action items
        instruction_prompt = f"""
        As a renowned delegation advisor, you specialize in coaching startup founders and CEOs on maximizing the effectiveness of their chief-of-staff and executive assistants (EAs). 

        You primarily use transcripts from an onboarding call with the founder/CEO to generate a list of initial delegation ideas you can recommend so that clients can get the ball rolling with their EA.

        Here is the transcript of {client}'s onboarding call, in <transcript></transcript> XML tags:

        <transcript>
        {transcript}
        </transcript>

        Please perform the following tasks: 
        1. Identify and extract any explicit or implicit action items for the client, {client}. In order to identify these action items, pay special attention to what {client} says are their professional and personal priorities, their difficulties, their inspiration, passion projects, and what their ideal week looks like.
        2. Identify if, among any of the action items, there is anything an Executive Assistant (EA) can do or help to get {client} started. In order to identify these action items, pay special attention to what {client} says they need help with, what energizes them, and what drains them.
        3. Identify if there are any related task ideas that the chief of staff or EA can suggest to {client} that isn't explicitly asked for but might be as valuable or more valuable.
        4. Make sure to recommend a mix of both personal and work-related action items so that the client spends his time holistically.
        5. Make sure that the action items you extract for {client} and the EA are simplified as much as possible so that it's actually actionable and can be done right away to create immediate value to {client}
        6. Use your knowledge of {client} to evaulate each extracted action item/task, and assess their level of impact, whether they are 'High impact', 'Medium impact', or 'Low impact'.
        7. Categorize each action item/task as either Personal or Work-related.
        8. Categorize them further into the following sub-categories. If the main category is Personal: Physical Health, Mental Health, Relationships, Personal Finance, Learning / PKM, Passion Projects, Experiences/Travel, and Bucket List. If the category is work: Admin, Finance, People, Marketing, Sales, Product, Engineering, and Operations.
        9. Provide your reasoning as to why you assessed them that way. Base your answers on what you know about {client}. Limit this to 3-5 sentences. 
        10. The format of your overall response should look like what's shown between the example below. Make sure to follow the formatting and spacing exactly. Do not include the <example></example> XML tags in your final output. 
        11. Generate at least 5 client action items, 5 EA action items, and 5 potential tasks.

        <example>
        #### CLIENT ACTION ITEMS:
        
        1. Review the spreadsheet and share insights with Daniel and the team
            - Impact: High
            - Main area: Work
            - Sub-area: Product
            - Context: In the call, Client highlighted the importance of data-driven decision making to reach his goal of expanding our portfolio by 20% this year. This review will help identify potential opportunities to achieve this target.
        
        2. Collaborate on researching and understanding AI tools and their impact on venture capital firms
            - Impact: High
            - Main area: Work
            - Sub-area: Operations
            - Context: Client expressed the need to stay at the forefront of technology trends, especially AI, due to an increasing number of tech-focused startups in our investment portfolio. This research collaboration aligns directly with that objective.
        
        3. Contribute to designing a Google Doc to consolidate information on AI for venture capital firms
            - Impact: Medium
            - Main area: Work
            - Sub-area: Product
            - Context: Client wants to ensure that the entire team is on the same page about AI trends in the VC industry. This shared Google Doc will help consolidate all the research, serving as a go-to resource for the team
        
        4. Be prepared to discuss the topic with LPs, the team, and other stakeholders in the ecosystem
            - Impact: High
            - Main area: Work
            - Sub-area: People
            - Context: Client emphasized the importance of keeping LPs informed about our strategic focus on AI. He also noted that clear communication with stakeholders could help attract more AI-focused startups.


        #### EA ACTION ITEMS:
        1. Assist client in researching AI tools and their impact on the venture capital industry
            - Impact: High
            - Main area: Work
            - Sub-area: Product
            - Context: Client mentioned in the transcript that he is focusing on improving a specific skill each quarter (currently AI and coding). One of his weekly goals is to also connect with VCs more. Being able to improve his expertise in AI and the VC industry should hit two birds with one stone. He can leverage his skillset with AI in providing value to VCs. 
        2. Help gather and organize information in the Google Doc
            - Impact: Medium
            - Main area: Work
            - Sub-area: Admin
            - Context: During the call, Client stressed their preference for organized, easily accessible information. Assisting in managing this Google Doc will ensure he can quickly find the information they need.
        3. Support client in coordinating meetings and discussions with stakeholders when necessary
            - Impact: High
            - Main area: Work
            - Sub-area: People
            - Context: Client mentioned his tight schedule and the importance of efficient time management. Your support in organizing meetings will allow him to focus on strategic tasks and maintain productive relationships with stakeholders.
            
        #### POTENTIAL TASKS:
        1. Suggest to client to hold a workshop/validation session with relevant team members to explore AI tools and processes in their respective department
            - Impact: Medium
            - Main area: Work
            - Sub-area: People
            - Context: As client aims to create a company-wide understanding of AI's potential, this workshop could accelerate the learning process and ensure all teams are equipped to leverage AI in their work.
        2. Recommend incorporating AI tools into each team's operations to streamline workflows and improve efficiency
            - Impact: High
            - Main area: Work
            - Sub-area: Operations
            - Context: Client mentioned his goal of increasing operational efficiency by 15%. Recommending AI tool incorporation could be a strategic step towards achieving this.
        3. Explore partnerships with AI solution providers specifically targeting venture capital firms or their portfolio companies to stay ahead in competition
            - Impact: High
            - Main area: Work
            - Sub-area: Product
            - Context: In the call, client mentioned wanting to give our portfolio companies an edge through AI. Partnering with AI solution providers could be a key strategy in realizing this objective.
        4. Keep an eye on competitors or other venture capital firms adopting AI technology and their success to gather case studies and examples for future presentations
            - Impact: Medium
            - Main area: Work
            - Sub-area: Product
            - Context: Client was keen on understanding the competitive landscape better. Monitoring competitors' AI adoption can provide useful insights for future strategy and presentations.
        </example>
                
        Answer the question immediately without preamble. Do not start with 'Here are the suggested action items' or something like that. Just immediately provide the content.
        """

        
        # Run only if user has provided the client's name
        if client:
            instruction_progress_text = "Extracting your action items from the transcript... 🚀 Please wait."
            instruction_bar = st.progress(0, text=instruction_progress_text)
            action_items = process_transcript('instruction')
            for percent_complete in range(100):
                time.sleep(0.1)
                instruction_bar.progress(percent_complete + 1, text=instruction_progress_text)
            
            # Display delegation ideas to Streamlit
            st.success('Delegation ideas successfully extracted!', icon="✅") 
            st.write(action_items)


            # Prompt to analyze action items and determine the top 3 most important ones
            st.write("Analyzing and determing your top 3 action items...")

            evaluate_prompt = f"""
            As a renowned delegation advisor, you specialize in coaching startup founders and CEOs on maximizing the effectiveness of their chief-of-staff and executive assistants (EAs). 

            You've just finished an onboarding call with a client, {client}. 

            Here is the transcript, in <transcript></transcript> XML tags:

            <transcript>
            {transcript}
            </transcript>

            Here is a list of Client Action Items, EA Action Items, and Potential Tasks that you created based on that call, in <action_items>/action_items> XML tags:

            <action_items>
            {action_items}
            </action_items>
    
            Please perform the following tasks: 
            1. Based on the comprehensive evaluation you made, identify the top 3 action items that the client/EA should prioritize.
            2. Deepen the thought process. Break down the top 3 action items step-by-step and provide additional details for each step to make it easier for the chief-of-staff or EA. 
            3. Figure out what would be an implied next step after completing the task, which we can do pre-emptively, for the EA to demonstrate how proactive they are. 
            4. Generate potential questions that the EA might have for the client and predict how an elite entrepreneur would answer those questions. Also, consider any potential unexpected outcomes and how they might be handled. 
            5. The format of your overall response should look like what's shown between the example below. Make sure to follow the formatting and spacing exactly. Do not include the <example></example> XML tags in your final output. 


            <example>
            #### Top 3 Action Items:
            **ACTION ITEM:** Organize a list of people for Chris to talk to at Quiet Capital.
  
            **BREAKDOWN OF STEPS:**
            1. Understand the purpose of the meetings with the people at "yes". What does "yes" refer to? Is it a company or an event? 
            2. Define criteria for the people to be included in the list based on Chris's requirements.
            3. Research potential contacts at "yes" using networking sites like LinkedIn, or internal company resources.
            4. Create a spreadsheet or a document listing the names, positions, contact info, and any relevant notes about the contacts.
            5. Share this list with Chris and get his approval or feedback.

            **IMPLIED NEXT STEPS:**
            1. Schedule initial meetings with the people on the list based on Chris's availability.
            2. Prepare an agenda for each meeting, based on the purpose defined by Chris.

            **POTENTIAL QUESTIONS:**
            1. 'Who are the key people at "yes" that Chris would be interested in meeting?'
            - Chris might answer: 'I'm interested in meeting with people who have a significant influence on their operations and decision-making.'
            2. 'Are we looking for contacts in specific departments or across the entire organization?'
            - Chris might answer: 'I want to meet people from various departments to get a holistic understanding of their operations.'

            **POSSIBLE UNEXPECTED OUTCOMES:**
            1. Difficulty in finding contact info for people at "yes".
            - In such a case, the EA could reach out through official channels or use professional networking sites to request introductions.
            2. The people identified may not be available for a meeting.
            - The EA could propose alternatives or wait for their availability.

            ---

            **ACTION ITEM:** Coordinate the meetings Chris has mentioned with other teams.
  
            **BREAKDOWN OF STEPS:**
            1. Obtain the list of teams that Chris wants to meet and the purpose of each meeting.
            2. Plan a schedule keeping in mind the availability of Chris and the other teams.
            3. Send out meeting invites with necessary details such as date, time, location (or video call link), and agenda.
            4. Send a reminder to the attendees a day before the meeting.
            5. Gather and organize any materials or resources needed for the meeting.

            **IMPLIED NEXT STEPS:**
            1. Follow up on the meetings with minutes or a summary to all attendees.
            2. Schedule and coordinate subsequent meetings based on the needs identified in the initial meetings.

            **POTENTIAL QUESTIONS:**
            1. 'What are the objectives of these meetings?'
            - Chris might answer: 'The objective is to align with all the teams on our ongoing projects and to address any obstacles or challenges.'
            2. 'Is there a preferred order in which these meetings should be arranged?'
            - Chris might answer: 'No, the order is not crucial. What matters is that all meetings occur in a timely fashion.'

            **POSSIBLE UNEXPECTED OUTCOMES:**
            1. Difficulty in finding a common free slot for all team members.
            - In such a case, the EA can recommend splitting the meeting into smaller groups or suggest asynchronous communication methods.
            2. Unavailability of a meeting location.
            - The EA can arrange for a virtual meeting or find an alternate location.

            ---

            **ACTION ITEM:** Assist Chris in preparing and organizing information on the AI solutions.
  
            **BREAKDOWN OF STEPS:**
            1. Understand the context of AI solutions that Chris is interested in.
            2. Conduct research to gather information on the relevant AI solutions.
            3. Create a structured document or presentation that clearly outlines the information.
            4. Review the information with Chris and refine based on his feedback.

            **IMPLIED NEXT STEPS:**
            1. Proposing further research or subsequential actions based on the prepared information.
            2. Coordinating a presentation or a discussion session with the relevant team to discuss the AI solutions.

            **POTENTIAL QUESTIONS:**
            1. 'What specific areas of AI solutions are we focusing on?'
            - Chris might answer: 'We are focusing on AI solutions that can improve our operational efficiency and decision-making process.'
            2. 'How detailed should this information be?'
            - Chris might answer: 'It should be comprehensive enough to give us a clear understanding of the solutions and how they can be applied in our context.'

            **POSSIBLE UNEXPECTED OUTCOMES:**
            1. Difficulty in obtaining specific information on some AI solutions.
            - In such a case, the EA can reach out directly to AI solution providers for more detailed information or seek expertise from industry professionals.
            2. The information obtained might be too technical for non-technical team members.
            - The EA could work on simplifying the information or provide additional resources to help team members understand it better.
            </example>
                
            Answer the question immediately without preamble. Do not start with 'Here are the suggested action items' or something like that. Just immediately provide the content.
            """
            evaluate_progress_text = "Thinking really hard... 🤯 Please wait."
            evaluate_bar = st.progress(0, text=evaluate_progress_text)        
            top_items = process_transcript('evaluate')
            for percent_complete in range(100):
                time.sleep(0.1)
                evaluate_bar.progress(percent_complete + 1, text=evaluate_progress_text)
         
            # Display top 3 action items to Streamlit
            st.success('Top 3 action items successfully extracted!', icon="✅") 
            st.write(top_items)

            # Create a download button for the output
            combined_items = action_items + "\n" + top_items

            st.download_button(
                label="Download as text file",
                data=combined_items,
                file_name='delegation_ideas.txt',
                mime='text/plain',
            )
            
        else:
         st.warning("Please enter your client's name")     
    else:
        st.warning("Please upload a transcript before proceeding.")

