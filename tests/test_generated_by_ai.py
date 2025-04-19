It seems like you're looking for a way to track the status of tasks in your Celery task queue, but it's not clear what exactly you need help with. Could you please provide more details? Are you trying to monitor the progress of individual tasks or are you trying to track the overall health of your Celery setup?

If you want to track the status of each task as they run and complete in the queue, you could create a model like `TaskLog` that tracks these details. This would involve setting up a periodic task (using Django-Q or similar) that checks for any tasks that have not yet completed and attempts to update their status.

If you want to track overall health of your Celery setup, such as the number of failed tasks over time, this can be achieved by monitoring the `failed_tasks` table in your database. This would involve setting up a periodic task that checks for any entries in the `failed_tasks` table and logs these details.

If you could provide more specifics about what exactly you're trying to achieve, I might be able to give a more targeted answer.