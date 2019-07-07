Commands
===============

The following section outlines and explains the the commands for the bot. Below will show a usage and description for each command.

.. note::

    This page was last updated 6/26/2019. This page is not guarenteed to be updated and may not be update for a while.

General Commands
---------------------


.. data:: /about

    Shows info about the bot.


.. data:: /ping

    Shows the bot's latency.


.. data:: /userinfo [optional: user]

    Shows information on the user. When not mentioning a user, shows the command authors information.


.. data:: /serverinfo

    Shows information on the server.

.. data:: /docs

    Sends you the link to this page.


.. data:: /vote

    Shows bot list where you can upvote the bot, soon you will recieve perks for doing so.


Administrative Commands
---------------------


.. data:: /adword [word]

    This command adds a word to list of blocked words for the autmoderation module. The automod module must be turned on in order to work.


.. data:: /automod

    This command shows the available automod commands.


.. data:: /automod [on / off]

    This command turns the autmoderation module on or off, to turn on, simply do ``/automod on`` to turn off, do ``/automod on``. Automoderation is off by default.


.. data:: /automod inviteblocker

    Toggles the invite blocker feature for the server on and off. Default is off.


.. data:: /automod cursewords

    Toggles the blocked word feature for the server on and off. Default is off.


.. data:: /log

    This command shows the available logging commands.


.. data:: /log bulkmessagedelete

    Toggles the bulk_message_delete event. Default on.


.. data:: /log channelcreate

    Toggles the channel_create event. Default on.


.. data:: /log channeldelete

    Toggles the channel_delete event. Default on.


.. data:: /log memberban

    Toggles the member_ban event. Default on.


.. data:: /log memberjoin

    Toggles the member_join event. Default on.


.. data:: /log memberleave

    Toggles the member_leave event. Default on.


.. data:: /log memberunban

    Toggles the member_unban event. Default on.


.. data:: /log messagedelete

    Toggles the message_delete event. Default on.


.. data:: /log messageedit

    Toggles the message_edit event. Default on.


.. data:: /log rolecreate

    Toggles the role_delete event. Default on.


.. data:: /log roledelete 

    Toggles the role_delete event. Default on.


.. data:: /removeword [word]

    Removes a word from the list of blocked words.


.. data :: /words

    Lists all the blocked words in that server.


Moderation Commands
---------------------


.. data:: /ban [user] [optional: reason]

    Bans the specified/mentioned user.


.. data:: /kick [user] [optional: reason]

    Kicks the specified/mentioned user.


.. data:: /purge [ammount]

    Deletes the specified amount of messages.


.. data:: /deafen [user]

    Deafens the specified/mentioned user. They have to be in a voice channel!


.. data:: /undeafen [user]

    Undeafens the specified/mentioned user. They have to be in a voice channel!


.. data:: /nickname [user] [nickname]

    Sets the nickname of the specified/mentioned user. If a nickname is not specified, it will reset the nickname.


.. data:: /warn [user] [reason]

    Warns the specified/mentioned user.


.. data:: /warns [optional: user]

    Shows the specified members warns, if no user is mentioned, will show the warns for the author.
 

.. data:: /cases

    Shows the warns of the server or user.


.. data:: /case [case id]

    Shows information about the specified case.


.. data:: /reason [case id] [new reason]

    Edits the reason for the specified case.


.. data:: /addrole [user] [role]

    Adds a role to the specified member.


.. data:: /removerole [user] [role]

    Removes a role to the specified member.


.. data:: /mute [user] [reason]

    Mutes the specified member.


.. data:: /unmute [user] [reason]

    Un-mutes the specified member.


.. data:: /slowmode [delay time]

    Sets the slowmode to the specified number.


.. data:: /setlog

    Sets the log for the guild.


.. data:: /setmodlog

    Sets the modlog for the guild.

