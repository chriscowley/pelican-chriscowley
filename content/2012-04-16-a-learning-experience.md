---
layout: post
title: "A Learning Experience"
date: 2012-04-16 20:30
comments: true
categories: System Administration
---

How many times have you installed/updated a bit of software and read the line “Please take a back up” or something to that effect? 99 times out of a hundred, you will just continue and ignore it.
<!-- more -->

Today I had a reminder of why it is import to do so. I did a routine plug-in upgrade on our Jira installation (Customware Salesforce connector for those who want to know). I have done this several times, I had tested it in our Dev installation I was 100% confident it would work as expected. However, I actually decided to take a backup anyway.

I ran the upgrade in the production environment and re-indexed. Nothing out of the ordinary. 10% of the way into the index it fell over. Jira’s database was gone! Fortunately I was able to restore from my backup and at worst a comment or two was lost, but that still caused significant downtime.

I had done everything I could to make sure the upgrade would go smoothly, but it still did not. That is why software vendors always tell you to take a backup before even the smallest change – DO IT!

