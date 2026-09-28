import streamlit as st
import requests
import pandas as pd
from io import BytesIO


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide"
)


st.title("AI-Powered Resume Screening & Candidate Ranking System")
st.write("Upload resumes and compare them with a job description.")


st.subheader("Job Description")

job_description = st.text_area(
    "Enter Job Description",
    height=200,
    placeholder="Enter the complete job description here..."
)


st.subheader("Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if st.button("Screen Resumes", type="primary"):

    if not job_description.strip():
        st.error("Please enter a job description.")

    elif not uploaded_files:
        st.error("Please upload at least one resume.")

    else:

        files = []

        for uploaded_file in uploaded_files:

            files.append(
                (
                    "files",
                    (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                )
            )

        data = {
            "job_description": job_description
        }

        try:

            with st.spinner("Analyzing resumes..."):

                response = requests.post(
                    f"{API_URL}/screen-multiple-resumes",
                    data=data,
                    files=files,
                    timeout=300
                )

            if response.status_code == 200:

                result = response.json()

                candidates = result.get(
                    "candidates",
                    []
                )

                if not candidates:

                    st.warning("No candidates were processed.")
                    st.stop()

                st.success(
                    f"{len(candidates)} resume(s) processed successfully."
                )

                st.divider()

                col1, col2, col3 = st.columns(3)

                shortlisted = sum(
                    1
                    for candidate in candidates
                    if candidate["status"] == "Shortlisted"
                )

                average_score = sum(
                    candidate["match_score"]
                    for candidate in candidates
                ) / len(candidates)

                col1.metric(
                    "Total Candidates",
                    len(candidates)
                )

                col2.metric(
                    "Shortlisted",
                    shortlisted
                )

                col3.metric(
                    "Average Match Score",
                    f"{average_score:.2f}%"
                )

                st.subheader("Candidate Ranking")

                table_data = []

                for candidate in candidates:

                    table_data.append(
                        {
                            "Rank": candidate["rank"],
                            "Name": candidate["name"],
                            "Email": candidate["email"],
                            "Experience": f"{candidate['experience']} years",
                            "Match Score": f"{candidate['match_score']}%",
                            "Status": candidate["status"]
                        }
                    )

                df = pd.DataFrame(table_data)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Filters")

                filter_col1, filter_col2, filter_col3 = st.columns(3)

                all_skills = set()

                for candidate in candidates:

                    for skill in candidate["skills"]:
                        all_skills.add(skill)

                skill_options = [
                    "All"
                ] + sorted(all_skills)

                selected_skill = filter_col1.selectbox(
                    "Filter by Skill",
                    skill_options
                )

                min_experience = filter_col2.number_input(
                    "Minimum Experience",
                    min_value=0.0,
                    max_value=50.0,
                    value=0.0,
                    step=0.5
                )

                education_options = ["All"]

                all_education = set()

                for candidate in candidates:

                    for education in candidate["education"]:
                        all_education.add(education)

                education_options += sorted(all_education)

                selected_education = filter_col3.selectbox(
                    "Filter by Education",
                    education_options
                )

                filtered_candidates = []

                for candidate in candidates:

                    skill_match = (
                        selected_skill == "All"
                        or selected_skill in candidate["skills"]
                    )

                    experience_match = (
                        candidate["experience"] >= min_experience
                    )

                    education_match = (
                        selected_education == "All"
                        or selected_education in candidate["education"]
                    )

                    if (
                        skill_match
                        and experience_match
                        and education_match
                    ):
                        filtered_candidates.append(candidate)

                st.subheader("Filtered Candidates")

                filtered_data = []

                for candidate in filtered_candidates:

                    filtered_data.append(
                        {
                            "Rank": candidate["rank"],
                            "Name": candidate["name"],
                            "Email": candidate["email"],
                            "Skills": ", ".join(candidate["skills"]),
                            "Education": ", ".join(candidate["education"]),
                            "Experience": candidate["experience"],
                            "Match Score": candidate["match_score"],
                            "Status": candidate["status"]
                        }
                    )

                filtered_df = pd.DataFrame(
                    filtered_data
                )

                if not filtered_df.empty:

                    st.dataframe(
                        filtered_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    csv_data = filtered_df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        "Download CSV",
                        csv_data,
                        "shortlisted_candidates.csv",
                        "text/csv"
                    )

                    excel_buffer = BytesIO()

                    with pd.ExcelWriter(
                        excel_buffer,
                        engine="openpyxl"
                    ) as writer:

                        filtered_df.to_excel(
                            writer,
                            index=False,
                            sheet_name="Candidates"
                        )

                    st.download_button(
                        "Download Excel",
                        excel_buffer.getvalue(),
                        "shortlisted_candidates.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                else:

                    st.info(
                        "No candidates match the selected filters."
                    )

                st.divider()

                st.subheader("Candidate Details")

                candidate_names = [
                    candidate["name"]
                    for candidate in candidates
                ]

                selected_name = st.selectbox(
                    "Select Candidate",
                    candidate_names
                )

                selected_candidate = next(
                    candidate
                    for candidate in candidates
                    if candidate["name"] == selected_name
                )

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:

                    st.write(
                        f"**Name:** {selected_candidate['name']}"
                    )

                    st.write(
                        f"**Email:** {selected_candidate['email']}"
                    )

                    st.write(
                        f"**Experience:** {selected_candidate['experience']} years"
                    )

                    st.write(
                        f"**Education:** {', '.join(selected_candidate['education'])}"
                    )

                    st.write(
                        f"**Certifications:** {', '.join(selected_candidate['certifications'])}"
                    )

                with detail_col2:

                    st.metric(
                        "Match Score",
                        f"{selected_candidate['match_score']}%"
                    )

                    st.write(
                        f"**Skill Score:** {selected_candidate['skill_score']}%"
                    )

                    st.write(
                        f"**Experience Score:** {selected_candidate['experience_score']}%"
                    )

                    st.write(
                        f"**Semantic Score:** {selected_candidate['semantic_score']}%"
                    )

                    st.write(
                        f"**Status:** {selected_candidate['status']}"
                    )

                st.write(
                    "**Matched Skills:**",
                    ", ".join(selected_candidate["skills"])
                )

                st.write(
                    "**Missing Skills:**",
                    ", ".join(selected_candidate["missing_skills"])
                    if selected_candidate["missing_skills"]
                    else "None"
                )

            else:

                st.error(
                    f"API Error: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI backend. "
                "Make sure uvicorn is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )