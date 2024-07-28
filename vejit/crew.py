from crewai import Crew, Process
from agents import question_checker, answer_generator, frag, crag
from tasks import question_checking_task, answer_generation_task, frag_task, crag_task

crew = Crew(
    agents=[question_checker, answer_generator, frag, crag],
    tasks=[question_checking_task, answer_generation_task, frag_task, crag_task],
    process=Process.sequential,  # assuming hierarchical process is available
)

results = crew.kickoff(inputs={"query":'My steering wheel is making some noise?', "vehicle": "Tata Punch"})
print(results)