#!/usr/bin/python
#-*- coding: utf-8 -*-

def user_update_handler(backend, details, response, user=None, is_new=False, *args, **kwargs):
    user.steam_id = details['player']['steamid']
    user.username = details['username']
    user.nickname = details['player']['personaname']
    user.avatar_small = details['player']['avatar']
    user.avatar_medium = details['player']['avatarmedium']
    user.avatar_full = details['player']['avatarfull']
    user.personastate = details['player']['personastate']
    user.social_user = kwargs['social_user']
    user.save()
    #user.update_inventory()
    return user
