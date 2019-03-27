test.c

char *greplaceInt(char *buff, int bufflen, char *var, int newval)
{
	char tmp[128];
	snprintf(tmp, sizeof(tmp), "%d", newval);
	return greplace(buff, bufflen, var, tmp);
}


char *greplace(char *buff, int bufflen, char *var, char *newval)
{
	char* ptr;
	char* tail;
	char* tmp = NULL;

	if (var == NULL || var[0] == '\0')
		return buff;

	if (newval == NULL)
		return buff;

	if((ptr = strstr(buff, var)) != NULL)
	{
		tmp = malloc(bufflen+128);
		memset(tmp, 0, bufflen+128);
		strncpy(tmp, buff, bufflen);

		ptr = strstr(tmp, var);
		*ptr = '\0';

		tail = &buff[strlen(tmp)+strlen(var)];

		strcat(tmp, newval);
		strcat(tmp, tail);

		strncpy(buff, tmp, bufflen);
	}

	if(tmp != NULL)
		free(tmp);

	return buff;
}