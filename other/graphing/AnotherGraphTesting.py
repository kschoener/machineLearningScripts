import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

#test for making the legend clickable - only seeing certain days
def main():
	clickableTest()
	# eventHandlingTest()
#enddef main

'''
the goal of this is to set each day of the week clickable for the GraphData class
'''
def func(label):
    if label == '2 Hz':
        l0.set_visible(not l0.get_visible())
    elif label == '4 Hz':
        l1.set_visible(not l1.get_visible())
    elif label == '6 Hz':
        l2.set_visible(not l2.get_visible())
    plt.draw()
#enddef func

def clickableTest():
	t = np.arange(0.0, 2.0, 0.01)
	s0 = np.sin(2*np.pi*t)
	s1 = np.sin(4*np.pi*t)
	s2 = np.sin(6*np.pi*t)

	fig, ax = plt.subplots()
	l0, = ax.plot(t, s0, visible=False, lw=2)
	l1, = ax.plot(t, s1, lw=2)
	l2, = ax.plot(t, s2, lw=2)
	plt.subplots_adjust(left=0.2)

	rax = plt.axes([0.05, 0.4, 0.1, 0.15])
	check = CheckButtons(rax, ('2 Hz', '4 Hz', '6 Hz'), (False, True, True))

	check.on_clicked(func)

	plt.show()
#enddef clickableTest



def eventHandlingTest():
	t = np.arange(0.0, 0.2, 0.1)
	y1 = 2*np.sin(2*np.pi*t)
	y2 = 4*np.sin(2*np.pi*2*t)

	fig, ax = plt.subplots()
	ax.set_title('Click on legend line to toggle line on/off')
	line1, = ax.plot(t, y1, lw=2, color='red', label='1 HZ')
	line2, = ax.plot(t, y2, lw=2, color='blue', label='2 HZ')
	leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
	leg.get_frame().set_alpha(0.4)


	# we will set up a dict mapping legend line to orig line, and enable
	# picking on the legend line
	lines = [line1, line2]
	lined = dict()
	for legline, origline in zip(leg.get_lines(), lines):
	    legline.set_picker(5)  # 5 pts tolerance
	    lined[legline] = origline

	fig.canvas.mpl_connect('pick_event', onpick)

	plt.show()
#enddef eventHandlingTest


def onpick(event):
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    fig.canvas.draw()
#enddef onpick

if __name__ == '__main__':
	main()