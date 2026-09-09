import subprocess

class TaskScheduler:
    TASK_NAME = "NeteaseTimerTask"

    @staticmethod
    def create_wake_task(time_str, days="daily"):
        sc = "ONCE" if days == "once" else ("WEEKLY" if days != "daily" else "DAILY")
        day_param = ""
        if days == "mon-fri":
            day_param = '/d MON,TUE,WED,THU,FRI'
        elif days not in ("once","daily"):
            day_param = f'/d {days}'

        cmd = (
            f'schtasks /create /tn "{TaskScheduler.TASK_NAME}" '
            f'/tr "python your_exe_path --run-task" '
            f'/sc {sc} {day_param} /st {time_str} '
            f'/ru SYSTEM /rl HIGHEST /f /WAKE'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0

    @staticmethod
    def delete_task():
        subprocess.run(f'schtasks /delete /tn "{TaskScheduler.TASK_NAME}" /f', shell=True)

    @staticmethod
    def task_exists():
        r = subprocess.run(f'schtasks /query /tn "{TaskScheduler.TASK_NAME}"', shell=True, capture_output=True)
        return r.returncode == 0
