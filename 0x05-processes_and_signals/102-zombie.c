#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

/**
 * infinite_while - an infinite loop to keep the parent process running.
 *
 * Return: 0 on success.
 */
int infinite_while(void)
{
	while (1)
	{
		sleep(1);
	}
	return (0);
}

/**
 * main - creates 5 zombie processes.
 *
 * Return: Always 0 (Success)
 */
int main(void)
{
	pid_t pid;
	int i;

	for (i = 0; i < 5; i++)
	{
		pid = fork();

		if (pid == 0)
		{
			return (0);
		}
		else if (pid > 0)
		{
			printf("Zombie process created, PID: %d\n", pid);
		}
		else
		{
			perror("Fork failed");
			return (1);
		}
	}

	infinite_while();
	return (0);
}
