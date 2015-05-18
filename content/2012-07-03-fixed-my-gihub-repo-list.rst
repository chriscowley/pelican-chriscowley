Fixed my gihub repo list
########################
:tags:  programming

My Github repo list has not worked as all since I moved over to
Octopress. This evening I though I would have a little look into it. It
turned out that GitHub has depreciated the version 1 and 2 APIs.
Octopress was using version 2, so I have made a little change.

{%gist 3042647 %}

According to this issue there will be a fix in Octopress 2.1. However,
this patch will keep things working until Brandon Mathis moves it into
the master branch. Of course that issue also highlighted the fact that I
had just re-invented the wheel :(
