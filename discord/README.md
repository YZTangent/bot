# Ka.Y.E Discord bot

# Discord bot
## TO-DO
- [x] Bot has to talk to supabase somehow
  - [x] Instantiate Supabase Client
  - [x] Send row entry to Supabase every Startup for logging
- [x] Need tables on supabase to put events onto
- [ ] need supabase to automatically create a row for each existing user
- [ ] need elements on react app to interact with these tables 
- [ ] Google Calendar Integration
- [ ] ~~Graceful Shutdown~~
  - [ ] ~~Command Shutdown~~
- [ ] ~~Make command to have server registered with webapp~~

## Quick Access
- [Disnakes Documentation](https://docs.disnake.dev/en/latest/index.html)
- [Disnakes Slash Commands](https://docs.disnake.dev/en/latest/ext/commands/slash_commands.html)
- [Supabase Python Documentation](https://github.com/supabase-community/supabase-py)

## Thought Process

### Potential Problems
- How do you register a command locally instead of globally?

### Command Registration Logic


### Command Invocation Logic
- Guild
  - Role
    - Command
  - Role check fail path
- Guild check fail path

### Proposed table structure


| GuildID  | Command     | Role        | Instructions      |
|---       | ----------- | ----------- |  ---              |
| GuildID1 | Command 1   | RoleID 1    | Instructions 1    |
| GuildID1 | Command 2   | RoleID 2    | Instructions 2    |

# Milestone 3
- [ ] A command for users to have the bot send them a list of events they have RSVP’d to for purposes of keeping track. The list of events will include details on the event, such as the starting time as well as location if any.
- [ ] Inline bot capabilities such that the user can send invitations to events without having to add other users to the server. 
- [ ] The ability for the bot to share events across multiple servers. 
- [ ] The ability to bind words as triggers for a response, either text or an image, from the bot
  - /bind word url
  - inserts a row onto database table with guild_id, word, and url
  - bot loads dictionatry of guild_id to dictionary of words to lists of urls on startup/update
  - 
- [ ] Send messages to remind users of events at certain time intervals before the start of the event eg 1 day, 1 hour.
  - Check event table every day and pull events that match the guild
  - Send message to server if event is 1 day later
  - Create a task to send another message 23 hours later
- [ ] Allow users to register their birthdays and have the discord bot automatically send birthday announcements and/or create birthday events.
  - Execute on a per group basis
  - Lookup table every day???? (naive)
    - Look up on startup and on update commands

- [ ] Command which suggests activities/places to users based on keywords, such as outdoors, sporty, online, etc. (Tentative)
- [ ] Embedded link which allows users to demarcate available timings with a pop up window of a calendar. (Tentative)
- [ ] Administrator role checks for administrator commands
  - message.author.guild_permissions.administrator
  - 

## Bot Startup Routine
- [ ] Pull Birthdays



## Issues
- [ ] How do you send a message everyday
  - schedule module?
  - Ideas
    - Created Job
    - Store jobs, identified by group_id in a table
    - Each task has a name and id
    - unique identifier by group and name
  - 
- /remindme timeFromNow/freq what
  - birthdays and event remidners will be a subset of this


## Derivative ideas
- Daily/Weekly reminder
  - Option to ask for accoutn takeover
