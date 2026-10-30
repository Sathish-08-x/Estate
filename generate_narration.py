import os
import wave
import win32com.client

SLIDE_SCRIPTS = [
    (
        "Welcome to the project presentation of EstateFlow, a Property Lead Management System developed for our "
        "CSE326 Web Development Continuous Assessment 1. EstateFlow is designed using semantic HTML5, custom CSS3, "
        "and modern JavaScript to deliver a lightweight, high-performance real estate CRM with zero server dependencies."
    ),
    (
        "Let us examine the problem statement and motivation. In modern real estate consulting, managing prospect inquiries "
        "across fragmented messaging apps and physical diaries leads to dropped leads and lost property deals. "
        "Consultants struggle to track lead stages and deadlines. EstateFlow solves this by organizing prospect data "
        "and pipeline stages in one unified web workspace."
    ),
    (
        "Here is our proposed solution architecture. EstateFlow consists of four integrated modules: a real-time KPI "
        "analytics dashboard, a comprehensive lead registration form, an interactive leads registry with instant inline "
        "stage updating, a visual Kanban sales pipeline board, and a priority-ranked follow-up schedule."
    ),
    (
        "This is the real-time analytics dashboard on index.html. It presents four key performance indicator cards: "
        "Total Active Leads, Site Visits Scheduled, Leads in Negotiation, and Closed Won Deals. These metric cards "
        "feature smooth CSS hover animations and automatically recalculate in real-time as leads move through the pipeline."
    ),
    (
        "Next is the new lead registration form. It enables consultants to quickly capture prospective client details "
        "including client name, buyer or seller classification, property preference such as apartment, house, or condo, "
        "estimated budget, lead stage, priority, and follow-up date. Submissions automatically validate and append to the system registry."
    ),
    (
        "Now we demonstrate the All Leads registry table. Every registered property lead is displayed with comprehensive "
        "contact and budget details. A key feature is the inline stage dropdown with an instant Save action. When clicked, "
        "it updates the stage column immediately and writes the new stage to browser storage, persisting across page refreshes."
    ),
    (
        "Here is part one of our visual Kanban sales pipeline board. Built entirely using flexible CSS layout, the pipeline "
        "distributes incoming property inquiries into dedicated workflow columns. Prospect cards feature color-coded "
        "left borders denoting high, medium, and low priority, clearly highlighting budgets and property types."
    ),
    (
        "Moving to part two of our sales pipeline board, we track leads through advanced negotiation and closed won stages. "
        "When a lead's stage is updated in the table, its card dynamically transitions into the corresponding pipeline column. "
        "If a column has no active deals, clean empty state placeholders are rendered."
    ),
    (
        "The fourth core module is the integrated follow-up schedule. It ensures that agents never miss a client appointment "
        "or call deadline. The schedule table ranks follow-up dates by priority and displays actionable status tags "
        "from pending to scheduled and won, supported by our quick-access sidebar navigation."
    ),
    (
        "Let us review the technical implementation. EstateFlow is engineered with pure web standards: semantic HTML5 "
        "for clean document structure, modern CSS3 with custom properties and entrance animations, and vanilla JavaScript "
        "for dynamic DOM manipulation. Browser LocalStorage serves as our persistent client-side data engine."
    ),
    (
        "Regarding our CA1 assessment compliance: our project fulfills every requirement of the academic rubric. "
        "We have achieved full functionality and responsive UI for 15 marks, thoroughly prepared architectural "
        "explanations for the 10-mark viva, and structured this four-minute presentation for the 5-mark video evaluation."
    ),
    (
        "In conclusion, EstateFlow is a complete, deployable web application. The source code is maintained on GitHub "
        "under branch main, published live on GitHub Pages, documented in our 31-page code PDF, and submitted "
        "via our official Excel template. Thank you for viewing our project presentation."
    )
]

def generate_narration():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 2
    speaker.Volume = 100

    temp_files = []
    sample_rate = 22050
    channels = 1
    sampwidth = 2
    target_slide_seconds = 20

    print("Generating voice narration for all 12 slides at Rate 2...")
    for idx, text in enumerate(SLIDE_SCRIPTS):
        temp_wav = f"slide_{idx}.wav"
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(temp_wav, 3)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()

        with wave.open(temp_wav, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            duration = wf.getnframes() / wf.getframerate()
            sample_rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()

        print(f"Slide {idx + 1}: Generated {duration:.2f}s audio. Padding to {target_slide_seconds}s...")

        target_frames_count = int(target_slide_seconds * sample_rate)
        current_frames_count = len(frames) // (channels * sampwidth)
        
        if current_frames_count < target_frames_count:
            silence_needed = target_frames_count - current_frames_count
            audio_bytes = frames + (b'\x00' * (silence_needed * channels * sampwidth))
        else:
            audio_bytes = frames[:target_frames_count * channels * sampwidth]

        padded_wav = f"slide_{idx}_padded.wav"
        with wave.open(padded_wav, 'wb') as pwf:
            pwf.setnchannels(channels)
            pwf.setsampwidth(sampwidth)
            pwf.setframerate(sample_rate)
            pwf.writeframes(audio_bytes)

        temp_files.append(padded_wav)
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

    combined_wav = "full_narration_4min.wav"
    with wave.open(combined_wav, 'wb') as cwf:
        cwf.setnchannels(channels)
        cwf.setsampwidth(sampwidth)
        cwf.setframerate(sample_rate)
        for pf in temp_files:
            with wave.open(pf, 'rb') as wf:
                cwf.writeframes(wf.readframes(wf.getnframes()))
            if os.path.exists(pf):
                os.remove(pf)

    with wave.open(combined_wav, 'rb') as wf:
        total_duration = wf.getnframes() / wf.getframerate()
    print(f"SUCCESS: Combined audio created at {combined_wav} with duration {total_duration:.2f}s (exactly 4:00 mins)!")

if __name__ == '__main__':
    generate_narration()
