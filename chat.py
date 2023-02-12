import gpt_lib.notes as notes
import gpt_lib.nexus as nexus
import gpt_lib.i18n as i18n

CHAT_BOT_NAME   = i18n.translation('CHAT_BOT_NAME', i18n.LANGUAGE)
USER            = i18n.translation('USER', i18n.LANGUAGE)

NBR_CONV_MSG    = 4
NBR_MEMORIES    = 10

#
# Main chat bot loop for conversation
#

if __name__ == '__main__':

    #### load conversation
    conversations = nexus.load_convo()

    while True:
        #### get user input, save it, vectorize it, etc
        a = input('\n\n%s: ' % USER)
        vector = nexus.save_conversation(USER, a, conversations)

        #### compose corpus (fetch memories, etc)
        memories = nexus.fetch_memories(vector, conversations, NBR_MEMORIES)  # pull episodic memories

        # TODO - fetch declarative memories (facts, wikis, KB, company data, internet, etc)

        note = notes.summarize_memories(memories)

        # TODO - search existing notes first

        recent = nexus.get_last_messages(conversations, NBR_CONV_MSG)

        output = nexus.ask_theo(note, recent, a)

        nexus.save_conversation(CHAT_BOT_NAME, output, conversations)

        #### print output
        print('\n\n%s: %s' % (CHAT_BOT_NAME, output)) 