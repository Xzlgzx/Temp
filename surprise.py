import streamlit as st
import cv2
import time
from streamlit_lottie import st_lottie
import requests
import re

st.markdown(
    """
    <style>
    .stButton button {
        padding: 20px 40px;
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .big-text {
        font-size: 27px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .sidebar .sidebar-content .block-container .block-container {
        justify-content: flex-end;
        width: 40rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

QUESTIONS = re.split(r'\.|\?', """If you have an unlimited budget, what would your ideal dream home look like, both the exterior, interior and location?
Tell me the three luckiest moments of your life.
If you could name yourself again, what would it be (both English and Chinese)?
If you were to transform yourself into a mini caricature in a vending machine, what would it look like?
If you found a magic lamp with a genie, what three wishes would you make?
If you have the super power to create an imaginary job with any job duty you want it to have, what would it be?
If you could live in one specific era of history, when and where would you choose?
If you could design your perfect day from start to finish, how would it unfold?
What single moment stands out as encapsulating perfect happiness for you; what made it so joyous/meaningful?
If you knew you couldn't fail, what huge risks or ambitious goals would you take or set for yourself?
What meaningful impacts or lasting contributions do you deeply aspire to make while you're alive?
Give me the three must-dos you have in this life on your bucket list that exclude marriage, kids, and careers.
What is the most random and useless fact you know about?
What experiences, skills or perspectives do you have that you think are genuinely unusual or unconventional?
List the top 5 greatest moments of your life.
What is/are the proudest moment of your life, and is there something in life that could potentially make you feel even prouder?
What is the most random thing that you are obsessed with?
What is the one thing you would pick up if you could time-travel back to your childhood?
Is there a childhood hero, real or fictional, that inspired the types of roles you saw yourself in?
Give me your top three hobbies right now if time is not a problem at all.
What are the things you love the most about China?
What are your favourite meals, and what meals are your favourite to cook?
What is the most memorable dream you have had?
Who is/are your favourite or special person/people whom you know in this life, and why?
If you could choose to meet anyone in history, who would they be?
What do you wish your ideal life to look like at the age of 30, 50, and 80?
What’s the funniest thing you said that made your friends laugh the hardest?
Who is your best of best friend(s) in this life, and why do you think this is the case?
Give me the top 5-10 pieces of your favourite music that pop into your mind right now.
On a scale of 1-10, how high would you rate your life own life today, and what do you think would improve it and make it the most possible perfect life?
Would you rather maintain your mind or body today if you lived to 100?
What do you think I am thinking about right now?
What's the boldest lie you ever got away with telling as a kid?""")
QUESTIONS.pop()

NAME = "Miss Jiang"
COMPLIMENT = "princess of Nanyue Kingdom"
UNIQUE_PERSON_URL = "https://lottie.host/6a196f67-0804-4f78-825f-03a47c35330b/f0DdYNoCGa.json"
final_poem = """
Nerds often type lots of code,\n
To make a simple app.\n
It takes bugs and debugs,\n
To make the code thing sing.\n
For many days and nights I've been smashing,\n
For you.\n
To be sure I can still find my heart,\n
When the AI has slept."""

def starter():
    header_ph = st.title('Welcome to "Heart Surgeon":')
    text_ph = st.markdown('<h1 class="big-text">The end-to-end super-app for everything love-related.</h1>',
                unsafe_allow_html=True)

    st.sidebar.title("Options")

    if st.sidebar.button(
            "Happily married for 30 years but recently discovered my son isn't mine."):
        st.warning(
            "Be strong, my friend, because only men can make such a revealing discovery.")
    if st.sidebar.button("Newly-divorced after finding out I'm gay."):
        st.warning('Better open the closet earlier than later.')
    if st.sidebar.button(
            "Just got married, but low key have a crush on some girl at the coffee shop."):
        st.warning("Why not emigrate with both to Saudi Arabia?")
    if st.sidebar.button(
            "In a relationship, but accidentally went on a Tinder date last weekend."):
        st.warning("Why not make it a double-date next weekend?")
    key_button = st.sidebar.button("Getting to know someone.")
    if key_button:
        text_ph.empty()
        header_ph.title('"Waitttt, are you really sure you never met the guy in front of you before???" - The Buddha')
        st.button("Let's start!")
        return header_ph

    url = requests.get(
        "https://lottie.host/e2935061-f0b8-45fe-950f-f898fea7e9df/EgqKFASUuo.json")

    url_json = dict()

    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Error in the URL")

    st_lottie(url_json)

def detect_faces(person_type, lower, upper, further):
    # Streamlit app
    title_ph = st.empty()
    title_ph.title("Let's do a face detection to start the surprise! " + person_type)

    button_ph = st.empty()
    if button_ph.button("Start Face Detection"):

        # Open the camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Unable to open the camera.")
            return

        # Create a cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Start the camera loop
        start_time = time.time()
        progress = st.progress(0)  # Initialize the progress bar
        with st.spinner("Analyzing..."):  # Display the "Analyzing" animation
            frame_placeholder = st.empty()
            while time.time() - start_time < 5:
                # Read the frame from the camera
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read the camera frame.")
                    break

                # Convert the frame to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Display the frame with face detection
                cv2.imshow('Face Detection', frame)

                frame_placeholder.image(frame, channels="RGB") #delete

                # Update the progress bar based on elapsed time
                progress_value = min((time.time() - start_time) / 5, 1.0)
                progress.progress(progress_value)

                # Check for keyboard interrupt
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Release the camera and close the OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Set progress bar to 100%
        progress.progress(1.0)

        st.markdown(
            f"<h1 style='font-weight: bold; font-size: 26px; text-align: left;'>I am {lower}% confident that this person is a {COMPLIMENT}. {further}</h1>"
            , unsafe_allow_html=True)
        return True


def start_page(main_text, url, button_text):
    comp_1 = st.empty()

    comp_1.title(main_text)

    url = requests.get(url)

    url_json = dict()

    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Error in the URL")

    comp_2 = st.empty()

    button_clicked = comp_2.button(button_text, key="my_button",
                                   help="Wanna see what's next???")

    if not button_clicked:
        st_lottie(url_json)

    time.sleep(1.75)

    if button_clicked:
        comp_1.empty()
        comp_2.empty()
        return True


def game_intro_page():
    intro_ph = st.empty()
    intro_ph.title("Wanna start our game now?")

    button_ph = st.empty()

    if button_ph.button("Yes please!"):
        intro_ph.empty()
        button_ph.empty()
        return True

def play_game():
    current_question = st.session_state.get('current_question', 0)
    finished = st.session_state.get('finished', False)

    qa = st.sidebar.title("Q&A")
    question_ph = st.empty()
    question_ph.header(QUESTIONS[current_question])

    if finished and current_question == len(QUESTIONS) - 1:
        question_ph.empty()
        qa.empty()
        st.markdown(
            "<h1 style='font-weight: bold; font-size: 40px; text-align: left;'>{}</h1>".format(
                "The End"), unsafe_allow_html=True)
        for stanza in final_poem.split("\n"):
            st.markdown(
                "<h1 style='font-weight: bold; font-size: 28px; text-align: left;'>{}</h1>".format(
                    stanza), unsafe_allow_html=True)
    else:
        if st.sidebar.button("Next") and current_question < len(QUESTIONS) - 1:
            current_question += 1
            st.session_state['current_question'] = current_question
            if current_question == len(QUESTIONS) - 1:
                st.session_state['finished'] = True
            question_ph.header(QUESTIONS[current_question])
        if st.sidebar.button("Previous") and current_question > 0:
            current_question -= 1
            st.session_state['current_question'] = current_question
            question_ph.header(QUESTIONS[current_question])
        if st.sidebar.button("To End"):
            st.session_state['current_question'] = len(QUESTIONS) - 1
            st.session_state['finished'] = True
            st.experimental_rerun()

def main():
    # if "page_number" not in st.session_state:
    #     st.session_state.page_number = 1
    # if st.session_state.page_number == 1:
    #     confirmed = starter()
    #     if confirmed:
    #         st.session_state.page_number = 2
    # elif st.session_state.page_number == 2:
    #     confirmed = detect_faces("Ladies first!", 62.15432, 73.28437, "")
    #     if confirmed:
    #         button_ph = st.empty()
    #         st.session_state.page_number = 3
    #         if button_ph.button("Gentleman next!"):
    #             st.experimental_rerun()
    # elif st.session_state.page_number == 3:
    #     confirmed = detect_faces("Let's go my man!", 100, 100,
    #                              "He looks as stunning as the person before!")
    #     if confirmed:
    #         button_ph = st.empty()
    #         st.session_state.page_number = 4
    #         if button_ph.button("Let the fun start!!!"):
    #             st.experimental_rerun()
    # elif st.session_state.page_number == 4:
    #     time.sleep(4)
    #     confirmed = start_page("""Once upon a time, or more precisely on December 20th of 2023, in the land of weirdos...""", "https://lottie.host/4408d485-6835-45af-9afd-e0c3e38edf70/f9wGYZXutW.json", "*Next*")
    #     if confirmed:
    #         st.session_state.page_number = 5
    #         time.sleep(4)
    #         start_page(
    #             f"""And there comes a certain {NAME}. I surely don't know your birthday, yet, but I sure know a thing or two about......""",
    #             UNIQUE_PERSON_URL,
    #             "**Next**")
    # elif st.session_state.page_number == 5:
    #     game_intro_page()
    #     st.session_state.page_number = 6
    # else:
        play_game()

if __name__ == "__main__":
    main()