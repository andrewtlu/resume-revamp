import json
import re

def generate_resume_latex(template_file, json_file, output_file):
    # Load the LaTeX template
    with open(template_file, 'r') as file:
        template = file.read()

    # Load the JSON data
    with open(json_file, 'r') as file:
        resume_data = json.load(file)

    # Replace the placeholders in the template with the corresponding data
    template = template.replace('First Name (Nickname) Last Name', f"{resume_data['header']['name']}")
    template = template.replace('Emory Email Address', resume_data['header']['email'])
    template = template.replace('Phone Number', resume_data['header']['phone'])
    template = template.replace('www.linkedin.com/in/janehershman/', resume_data['header']['website'])

    # Education section
    education_section = ''
    for education in resume_data['education']:
        education_section += f"\\noindent\n\\textbf{{{education['school']}}} \\\\\n" #\\hfill {education['location']}
        degree_str = education['degree'] if 'degree' in education else ''
        if degree_str:
            education_section+= f"""\\emph{{{degree_str}}} \\hfill """
        # major_str = ', '.join(education['major']) if 'major' in education else ''
        # major_str = ''
        # if 'major' in education:
        #     major_list = [f"{major}" for major in education['major']]
        #     if len(major_list) > 1:
        #         major_list[-1] = f"\nDouble Major: {major_list[-1]}"
        #     major_str = ", ".join(major_list)
        # if major_str:
        #     education_section+= f"{major_str} "
        graduationDate_str = education['graduation'] if 'graduation' in education else ''
        if graduationDate_str:
            education_section += f"{graduationDate_str} \\\\ \n"
        start_end_date_str = education['start'] + ' -- ' + education['end'] if 'start' in education and 'end' in education else ''
        if start_end_date_str:
            education_section += f"{start_end_date_str} \n"
        gpa_str = education['gpa'] if 'gpa' in education else ''
        if gpa_str:
            education_section += f"Cumulative GPA: {gpa_str} \n"
        # if 'honors' in education:
        #     honors_list = [f"{honor}" for honor in education['honors']]
        #     honors_str = ", ".join(honors_list)
        # else:
        #     honors_str = ''
        # if honors_str:
        #     education_section += f"{honors_str} \\\\ \n"
        # relevant_courses_str = ''
        # if 'relevantCourses' in education and education['relevantCourses']:
        #     for course in education['relevantCourses']:
        #         relevant_courses_list = [f"{course}" for course in education['relevantCourses']]
        #         relevant_courses_list = ", ".join(relevant_courses_list)
        #     relevant_courses_str += f"{{Relevant Courses:}} {relevant_courses_list}"
        # if relevant_courses_str:
        #     education_section += f"\\emph{relevant_courses_str} "
        # attendedDates_str = education['attendedDate'] if 'attendedDate' in education else ''
        # if attendedDates_str:
        #     education_section += f"\\hfill {attendedDates_str} \n"
        details = education['details'] if 'details' in education else ''
        if details:
            details_str = f"\\begin{{itemize}}\n"
            for detail in details:
                details_str += f"\\item {detail}\n"
            details_str += f"\\end{{itemize}}"
        if details_str:
            education_section += f"{details_str}"
    education_section += f"\n \\vspace{{-\\baselineskip}}"
    education_section=education_section.replace(r'&', r'\&')
    pattern = r"\\section\*{\\large\\textbf{EDUCATION}.*(?=\\section\*{\\large\\textbf{WORK EXPERIENCE})"
    replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
    template = template.replace(replacement, f'\\section*{{\\large\\textbf{{EDUCATION}}}}\n\\vspace{{-\\baselineskip}}\n\\noindent\\rule{{\\textwidth}}{{0.4pt}}\n\n{education_section}\n')

    # Work Experience section
    work_experience_section = ''
    for experience in resume_data['experience']:
        work_experience_section += f"""
\\noindent
\\textbf{{{experience['company']}}} \\hfill {experience['location']}\\\\
\\emph{{{experience['position']}}} \\hfill {experience['start']} -- {experience['end']}
\\begin{{itemize}}
    {"\n\t".join([f"\\item {responsibility}" for responsibility in experience['description']])}
\\end{{itemize}}
"""
    work_experience_section += f"\n \\vspace{{-\\baselineskip}}"
    work_experience_section=work_experience_section.replace(r'&', r'\&')
    work_experience_section=work_experience_section.replace(r'%', r'\%')
    work_experience_section=work_experience_section.replace(r'$', r'\$')
    pattern = r"\\section\*{\\large\\textbf{WORK EXPERIENCE}.*(?=\\section\*{\\large\\textbf{PROJECTS})"
    replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
    template = template.replace(replacement, f'\\section*{{\\large\\textbf{{WORK EXPERIENCE}}}} \n \\vspace{{-\\baselineskip}} \n\\noindent\\rule{{\\textwidth}}{{0.4pt}} \n\n{work_experience_section}')
    print('work experience section successfully replaced')

    # projects section
    projects_section = ''
    for project in resume_data['projects']:
        projects_section += f"""
\\noindent
\\textbf{{{project['name']}}}
\\begin{{itemize}}
    {"\n\t".join([f"\\item {description}" for description in project['description']])}
\\end{{itemize}}
\\emph{{Technologies:}} {', '.join(project['technologies'])}
"""
    projects_section += f"\n \\vspace{{-\\baselineskip}}"
    projects_section=projects_section.replace(r'&', r'\&')
    projects_section=projects_section.replace(r'%', r'\%')
    projects_section=projects_section.replace(r'$', r'\$')
    pattern = r"\\section\*{\\large\\textbf{PROJECTS}.*(?=\\section\*{\\large\\textbf{EXTRACURRICULARS})"
    replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
    template = template.replace(replacement, f'\\section*{{\\large\\textbf{{PROJECTS}}}}\n\\vspace{{-\\baselineskip}}\n\\noindent\\rule{{\\textwidth}}{{0.4pt}}\n\n{projects_section}\n')
    print('projects section successfully replaced')

    # Extracurriculars section
    extracurriculars_section = ''
    for extracurricular in resume_data['extracurriculars']:
        extracurriculars_section += f"""
\\noindent
\\textbf{{{extracurricular['organization']}}} \\hfill {extracurricular['location']} \\\\
\\emph{{{extracurricular['position']}}} \\hfill {extracurricular['start']} -- {extracurricular['end']}
\\begin{{itemize}}
    {"\n\t".join([f"\\item {descriptor}" for descriptor in extracurricular['description']])}
\\end{{itemize}}
"""
    extracurriculars_section += f"\n \\vspace{{-\\baselineskip}}"
    extracurriculars_section=extracurriculars_section.replace(r'&', r'\&')
    extracurriculars_section=extracurriculars_section.replace(r'%', r'\%')
    extracurriculars_section=extracurriculars_section.replace(r'$', r'\$')
    pattern = r"\\section\*{\\large\\textbf{EXTRACURRICULARS}.*(?=\\section\*{\\large\\textbf{ADDITIONAL INFORMATION})"
    replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
    template = template.replace(replacement, f'\\section*{{\\large\\textbf{{EXTRACURRICULARS}}}}\n\\vspace{{-\\baselineskip}}\n\\noindent\\rule{{\\textwidth}}{{0.4pt}}\n\n{extracurriculars_section}\n')
    print('extracurriculars section successfully replaced')

    # Additional Information section
    additional_info_section = ''
    for activity in resume_data['other']:
        additional_info_section += f"\\noindent\n\\textbf{{{activity['title']}}}: "
        additional_info_section += ", ".join(activity['content']) + "\\\\ \n"

    additional_info_section=additional_info_section.replace(r'&', r'\&')
    additional_info_section=additional_info_section.replace(r'%', r'\%')
    additional_info_section=additional_info_section.replace(r'$', r'\$')
    pattern = r"\\section\*{\\large\\textbf{ADDITIONAL INFORMATION}.*(?=\\end{document})"
    replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
    template = template.replace(replacement, f'\\section*{{\\large\\textbf{{ADDITIONAL INFORMATION}}}}\n\\vspace{{-\\baselineskip}}\n\\noindent\\rule{{\\textwidth}}{{0.4pt}}\n\n{additional_info_section}\n')
    template = template.replace(r'#', r'\#')

#
#     # Additional Information section
#     additional_info_section = ''
#     additional_info_section += "\\noindent\\textbf{{Other Activities:}} " + ", ".join(resume_data['additionalInformation']['otherActivities']) + "\\\\\n"
#     additional_info_section += "\\noindent\\textbf{{Honors \\& Awards:}} " + ", ".join(resume_data['additionalInformation']['honors']) + "\\\\\n"
#     additional_info_section += "\\noindent\\textbf{{Skills:}} " + ", ".join(resume_data['additionalInformation']['skills']) + "\\\\\n"
#     additional_info_section += "\\noindent\\textbf{{Interests:}} " + ", ".join(resume_data['additionalInformation']['interests'])
#     additional_info_section=additional_info_section.replace(r'&', r'\&')
#     additional_info_section=additional_info_section.replace(r'%', r'\%')
#     additional_info_section=additional_info_section.replace(r'$', r'\$')
#     pattern = r"\\section\*{\\large\\textbf{ADDITIONAL INFORMATION}.*(?=\\end{document})"
#     replacement = re.search(pattern, template, flags=re.DOTALL).group(0)
#     template = template.replace(replacement, f'\\section*{{\\large\\textbf{{ADDITIONAL INFORMATION}}}}\\vspace{{-\\baselineskip}}\\noindent\\rule{{\\textwidth}}{{0.4pt}}{additional_info_section}')

    # Write the output to a new LaTeX file
    with open(output_file, 'w') as file:
        file.write(template)


if __name__ == "__main__":
    #TODO fix these paths for general use
    template_file_path = "dat/resume_template/bba_resume_template.tex"
    json_file_path = "src/tmp_resume.json"
    generate_resume_latex(template_file_path, json_file_path, 'dat/output/resume_latex.tex')
