from jenkins import Jenkins
import pprint

jenkins = Jenkins('http://ci.attentec.se')

jobs = jenkins.get_job_info("Hacka-Traffic-Light", 0, False)
last_completed_job = jobs["lastCompletedBuild"]
build_number = last_completed_job["number"]
build_info = jenkins.get_build_info("Hacka-Traffic-Light", build_number) 
result = build_info["result"]

pprint.pprint(result)
