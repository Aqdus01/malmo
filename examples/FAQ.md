# Frequently Asked Questions

## Known issues:
1, As the training progresses on an instance Malmo have the tendency to slow down. For a longer training resetting the environments at times can solve this issue.

## Common problems and potential solutions:

1, **Wrong java installation**: The version of Minecraft used in Malmo only supports JAVA version 8. As the gradle build script uses the $JAVA_HOME variable it should also point to the correct version.

2, **PermissionDenied** on the launchScript: the launch script has the wrong permission can change it on a unix based system with ```chmod 755 <launchScript>```

3, **Gradle: Could not acquire lock**: A previous gradle build has not released the lock. A solution can be to remove the cached files, they can be found under ```~/.gradle/caches``` executing ```rm -r ~/.gradle/caches``` can solve this issue.

4, **RLlib - RunTimeError: Error raised reading from queue**: Malmo runs a bit slower than what RLlib assumes with its default settings. Increasing the ```learner_queue_timeout``` parameter to the algorithm might solve this issue. The default parameter is set to 300 seconds.

5, **BUS error**: Hardware related issue, could be not enough RAM to run Malmo. Note that the memory usage can increase over time with Malmo.

## Tips
1, Creating a launch script: Make sure that you put it in the ```Minecraft/``` subdirectory and change the file's permission to executable. (On UNIX systems ```chmod 755 launchScript.sh``` should work)

2, For debugging sometimes it's easier to keep the Minecraft instances open and not use the launcher at each run.

3, If malmoenv does not seem to run on your system you should try to run the ```launchClient.sh``` script in ```Minecraft/``` first and observe the output in console.
