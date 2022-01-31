import backtrader as bt
# Create a Stratey
class FiboBB(bt.Indicator):

    alias = ('FiboBB',)
    lines = ('mid', 't1','t2','t3','t4','t5','t6', 'b1','b2','b3','b4','b5','b6',)
    params = (
        ('period', 50),      # Look Back Period
        ('devfactor', 3.0),  # standard dev. for extreme lines
        ('movav', bt.ind.MovingAverageSimple),
    )

    plotinfo = dict(
        subplot=False,
        plotlinelabels=False,
    )

    plotlines = dict(
        mid=dict(ls='--'),
        t1=dict(_samecolor=True),
        t2=dict(_samecolor=True),
        t3=dict(_samecolor=True),
        t4=dict(_samecolor=True),
        t5=dict(_samecolor=True),
        t6=dict(_samecolor=True),
        b1=dict(_samecolor=True),
        b2=dict(_samecolor=True),
        b3=dict(_samecolor=True),
        b4=dict(_samecolor=True),
        b5=dict(_samecolor=True),
        b6=dict(_samecolor=True),
    )

    def __init__(self):
        self.lines.mid = ma = self.p.movav(self.data, period=self.p.period)
        stddev = self.p.devfactor * bt.ind.StandardDeviation(self.data, ma, period=self.p.period,
                                           movav=self.p.movav)
        self.lines.t1 = ma + stddev
        self.lines.t2 = ma + stddev*.764
        self.lines.t3 = ma + stddev*.618
        self.lines.t4 = ma + stddev*.5
        self.lines.t5 = ma + stddev*.382
        self.lines.t6 = ma + stddev*.236
        self.lines.b1 = ma - stddev
        self.lines.b2 = ma - stddev*.764
        self.lines.b3 = ma - stddev*.618
        self.lines.b4 = ma - stddev*.5
        self.lines.b5 = ma - stddev*.382
        self.lines.b6 = ma - stddev*.236

        super(FiboBB, self).__init__()


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.FiboBBLines = FiboBB(self.data)

if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=False)
    data = bt.feeds.YahooFinanceCSVData(dataname='AAPL.csv')
    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy)
    cerebro.run()
    cerebro.plot(style='candlestick',bardown='black',barupfill = False,bartrans = 1.0,barup='black',volume=False)