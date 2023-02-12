import gpt_lib.notes as notes
import gpt_lib.nexus as nexus
from unidecode import unidecode

#
# Main chat bot loop for conversation
#

if __name__ == '__main__':

    #### load conversation
    conversations = nexus.load_convo()

    while True:
        #### get user input, save it, vectorize it, etc
        a = input('\n\nUTILISATEUR: ')
        vector = nexus.save_conversation('UTILISATEUR', a, conversations)

        #### compose corpus (fetch memories, etc)
        memories = nexus.fetch_memories(vector, conversations, 10)  # pull episodic memories

        # TODO - fetch declarative memories (facts, wikis, KB, company data, internet, etc)

        note = notes.summarize_memories(memories)

        # TODO - search existing notes first

        recent = nexus.get_last_messages(conversations, 4)

        output = nexus.ask_theo(note, recent, a)

        nexus.save_conversation('THEO', output, conversations)

        #### print output
        print('\n\nTHEO: %s' % output) 