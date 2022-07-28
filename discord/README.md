# This is cringe

## TO-DO
- [ ] Literally everything lmFAO
    - [x] Bot has to talk to supabase somehow
      - [x] Instantiate Supabase Client
      - [x] Send row entry to Supabase every Startup
    - [ ] Need tables on supabase to put stuff onto
      - [ ] need supabase to automatically create a row for each existing user
      - [ ] need elements on react app to interact with these tables 
    - [ ] Google Calendar Integration
    - [ ] Graceful Shutdown
      - [ ] Command Shutdown
    - [ ] Make command to have server registered with webapp

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