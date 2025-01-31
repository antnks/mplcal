import matplotlib
matplotlib.use('Agg')

import calendar
import matplotlib.pyplot as plt

class DayNotInMonthError(ValueError):
    pass

class MplCalendar(object):
    def __init__(self, year, month):
        calendar.setfirstweekday(6)

        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(year, month)
        # A month of events are stored as a list of lists of list.
        # Nesting, from outer to inner, Week, Day, Event_str
        # Save the events data in the same format
        self.events = [[[] for day in week] for week in self.cal]
        self.colors = [[None for day in week] for week in self.cal]

        self.w_days = 'Sun Mon Tue Wed Thu Fri Sat'.split()
        self.m_names = 'January February March April May June July August September October November December'.split()

    def _monthday_to_index(self, day):
        '''The 2-d index of the day in the list of lists.

        If the day is not in the month raise a DayNotInMonthError,
        which is a subclass of ValueError.

        '''
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
         # couldn't find the day
        raise DayNotInMonthError("There aren't {} days in the month".format(day))

    def add_event(self, day, event_str):
        'Add an event string for the specified day'
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append(event_str)

    def color_day(self, day, color):
        'Set square for specified day to specified color'
        week, w_day = self._monthday_to_index(day)
        self.colors[week][w_day] = color
        

    def _render(self, sizew=11, sizeh=8.5, sizedpi=80, **kwargs):
        'create the calendar figure'
        plot_defaults = dict(
            sharex=True,
            sharey=True,
            figsize=(sizew, sizeh),
            dpi=sizedpi,
        )
        plot_defaults.update(kwargs)
        f, axs = plt.subplots(
            len(self.cal), 7,
            **plot_defaults
        )
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                if self.colors[week][week_day] is not None:
                    ax.set_facecolor(self.colors[week][week_day])
                if self.cal[week][week_day] != 0:
                    ax.text(.02, .98,
                            str(self.cal[week][week_day]),
                            verticalalignment='top',
                            horizontalalignment='left')
                contents = "\n".join(self.events[week][week_day])
                ax.text(.03, .85, contents,
                        verticalalignment='top',
                        horizontalalignment='left',
                        fontsize=9)

        # use the titles of the first row as the weekdays
        for n, day in enumerate(self.w_days):
            axs[0][n].set_title(day)

        # Place subplots in a close grid
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        f.suptitle(self.m_names[self.month-1] + ' ' + str(self.year),
                   fontsize=20, fontweight='bold', y=0.95)

    def show(self, **kwargs):
        'display the calendar'
        self._render(**kwargs)
        plt.show()


    def save(self, filename, sizew=11, sizeh=8.5, sizedpi=80, **kwargs):
        'save the calendar to the specified image file.'
        self._render(sizew, sizeh, sizedpi, **kwargs)
        plt.savefig(filename)
