import SchemDraw as schem
import SchemDraw.elements as e
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


fig = figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_axes([0, 0, 1, 1])
plt.axis('equal')
plt.hlines(0, 0, 10, linestyles='--', colors='r')

d = schem.Drawing()
d.add(e.DOT_OPEN, xy=[3, 1], rgtlabel='300 K')
d.add(e.LINE, d='down', toy=0)
d.add(e.DOT)
d.add(e.RBOX, d='down', botlabel='0 dB\n40 K')
d.add(e.RBOX, d='down', botlabel='20 dB')
d.add(e.RBOX, d='down', botlabel='10 dB')
d.add(e.RBOX, d='down', botlabel='10 dB')
d.add(e.RBOX, d='down', botlabel='20 dB')
d.add(e.DOT_OPEN)

d.add(e.DOT_OPEN, xy=[7, 1], rgtlabel='300 K')
d.add(e.LINE, d='down', toy=0)
d.add(e.DOT)
d.add(e.RBOX, d='down', botlabel='0 dB\n40 K')
d.add(e.RBOX, d='down', botlabel='20 dB')
d.add(e.RBOX, d='down', botlabel='0 dB')
d.add(e.RBOX, d='down', botlabel='10 dB')
d.add(e.RBOX, d='down', botlabel='10 dB')
d.add(e.DOT_OPEN)



d.draw(ax=ax)



# plt.show()
d.save('testschematic.eps')