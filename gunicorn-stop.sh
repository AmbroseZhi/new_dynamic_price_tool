#!/bin/bash

ps auwx | grep gunicorn | grep -v 'grep' | awk {'print $2'} | while read i ; do 
	kill -9 ${i} 
done

