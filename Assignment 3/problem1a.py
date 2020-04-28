from mrjob.job import MRJob
import math
from mrjob.step import MRStep

class MRValueAvg(MRJob):
    def mapper(self,_,line):
        value=float(line.split('\t')[2])
        yield ('value', (value))
    def combiner(self, _, values):
        value=[]
        value2=[]
        for n in values:
            value.append(n)
            value2.append(n*n)
        yield('min', min(value))
        yield('max', max(value))
        yield('count_sum_sum2',(len(value),sum(value), sum(value2)))
    def reducer(self,key,values):
        count, sum, sum2 =0, 0, 0
        if key=='min':
            global mini
            mini=min(values)
            yield('min', mini)
        elif key=='max':
            global maxi
            maxi=max(values)
            yield('max', maxi)
        elif key=='count_sum_sum2':
            for c, s, s2 in values:
               count+=c
               sum+=s
               sum2+=s2
            avg=sum/count
            yield('avg', avg)
            std=((sum2-2*sum*avg+avg*avg*count)/count)**0.5
            yield('std',std)

    #
    # def mapper_bin(self,key,line):
    #     def bins(self, n, value):
    #         global maxi, mini
    #         window = (maxi - mini) / n
    #         minimun = mini
    #         bins = []
    #         for n in range(10):
    #             bins.append(mini)
    #             minimun += window
    #         if mini <= value <= bins[0]:
    #             return 'bin1'
    #         elif bins[0] < value <= bins[1]:
    #             return 'bin2'
    #         elif bins[1] < value <= bins[2]:
    #             return 'bin3'
    #         elif bins[2] < value <= bins[3]:
    #             return 'bin4'
    #         elif bins[3] < value <= bins[4]:
    #             return 'bin5'
    #         elif bins[4] < value <= bins[5]:
    #             return 'bin6'
    #         elif bins[5] < value <= bins[6]:
    #             return 'bin7'
    #         elif bins[6] < value <= bins[7]:
    #             return 'bin8'
    #         elif bins[7] < value <= bins[8]:
    #             return 'bin9'
    #         elif bins[8] < value <= maxi:
    #             return 'bin10'
    #     value=line.split('\t')[2]
    #     global binNum
    #     bin=bins(binNum,value)
    #     yield (bin, 1)
    #
    # def combiner_bin(self, _, values):
    #         yield(bin, sum(values))
    #
    # def reducer_bin(self, _, values):
    #         yield(bin, sum(values))

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer),
                MRStep(combiner=self.combiner_bin, reducer=self.reducer_bin) ]

if __name__ == "__main__":
    maxi, mini = MRValueAvg.run()


