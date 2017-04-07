from jenkins_get_last_completed_build_status import get_jenkins_build_info, SERVER_URL, JOB_NAME
import pprint
import datetime


def get_build_progress(build):
	estimated_duration = build["estimatedDuration"] / 1000
	build_timestamp = build["timestamp"] / 1000 - 1
	current_time = datetime.datetime.timestamp(datetime.datetime.now())

	time = max(0, current_time - build_timestamp)
	progress = 100 *  time / estimated_duration

	return min(progress, 100)

if __name__ == "__main__":
	jenkins = Jenkins(SERVER_URL)

	pprint.pprint(get_build_progress(get_jenkins_build_info(jenkins, JOB_NAME, "lastBuild")))