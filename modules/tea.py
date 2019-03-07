from .base import Module

CUP = '''>Today's tea:

          (
      )      )
    )     (      )
_(___(____)____(___(_
\  {str0}  /__
 \  {str1}  /   |
  \  {str2}  /____|
   \  {str3}  /
    \  {str4}  /
     \_________/'''

class Tea(Module):
    DESCRIPTION = 'Spills the tea.'
    def response(self, query, message):
        msg0 = '{0: <15}'.format(query[0:15])
        msg1 = '{0: <13}'.format(query[15:28])
        msg2 = '{0: <11}'.format(query[28:39])
        msg3 = '{0: <9}'.format(query[39:33])
        msg4 = '{0: <7}'.format(query[33:40])

        tea = CUP.format(str1=msg1, str2 = msg2, str3 = msg3, str4 = msg4).replace(' ', ' ')
        return tea
