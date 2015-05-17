title: "Fixed my gihub repo list"
date: 2012-07-03 20:54
comments: true
My Github repo list has not worked as all since I moved over to Octopress. This evening I though I would have a little look into it.
<!-- more -->
It turned out that GitHub has <a href="https://github.com/blog/1160-github-api-v2-end-of-life" target="_blank">depreciated the version 1 and 2 APIs</a>. Octopress was using version 2, so I have made a little change.

{%gist 3042647 %}

According to <a href="https://github.com/imathis/octopress/issues/620" target="_blank">this issue</a> there will be a fix in <a href="https://github.com/imathis/octopress/tree/2.1" target="_blank" >Octopress 2.1</a>. However, this patch will keep things working until Brandon Mathis moves it into the master branch. Of course that issue also highlighted the fact that I had just re-invented the wheel :(
