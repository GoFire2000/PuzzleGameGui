
import os
class DfsFinder():
    def __init__(self, oriBlocks, K, oriPath):
        self.K = K
        self.blocks = []
        self.dx = [-1, 1, 0, 0] # 移动方向，顺序有关
        self.dy = [0, 0, -1, 1]
        self.zeroX = 0
        self.zeroY = 0
        for i in range(K):
            self.blocks.append([])
            for j in range(K):
                self.blocks[i].append(oriBlocks[i][j])
                if self.blocks[i][j] == 0:
                    self.zeroX = i
                    self.zeroY = j
        self.ansPath =  []
        if self.K > 4 or len(oriPath) > 14:
            self.ansPath = [x for x in oriPath]
            self.ansPath = list(reversed(self.ansPath))

        self.copyPath = [x for x in oriPath]
        self.copyPath = list(reversed(self.copyPath))

        self.MaxStep = len(oriPath)
        path = []
        self.MinStep = self.MaxStep
        self.mp = dict()
        
        self.Dfs(self.zeroX, self.zeroY, 0, path)
    
    # 将图哈希，避免找到一样的图
    def hash(self):
        mod = 1231235345321215121
        hashV = 0
        for i in range(self.K):
            for j in range(self.K):
                hashV = hashV * self.K * self.K + self.blocks[i][j]
                hashV = hashV % mod
        return hashV

    # 判断是否成功
    def judgeOk(self):
        for i in range(self.K):
            for j in range(self.K):
                if i == self.K - 1 and j == self.K - 1:
                    if self.blocks[i][j] != 0:
                        return 0
                elif self.blocks[i][j] != i * self.K + j + 1:
                    return 0
        return 1
    
    # 拼图游戏剪枝策略，不修改已经完整的前几行
    def calcRightLine(self):
        for i in range(self.K):
            for j in range(self.K):
                if i == self.K - 1 and j == self.K - 1:
                    if self.blocks[i][j] != 0:
                        return i - 1
                elif self.blocks[i][j] != i * self.K + j + 1:
                    return i - 1
        return -1

    def Dfs(self, x, y, step, path):

        # tag = 0
        # for i in range(min(step, len(self.copyPath))):
        #     if path[i] != self.copyPath[i]:
        #         tag = 1
        # if tag == 0:    
        #     print(path)
        #     print(self.copyPath)
        #     print('----')
        
        if len(self.ansPath): # 找到可行解
            return
        if step > self.MaxStep: # 超出最大步数边界
            return
        if x == self.K - 1 and y == self.K - 1 and self.judgeOk() == 1: # 找到答案
            if step <= self.MinStep:
                self.MinStep = step
                self.ansPath = [x for x in path]
            return
        line = self.calcRightLine() # 剪枝，不修改已经完整的前几行
        dic = dict() # 剪枝，优先调整离自己正确位置最远的块
        for d in range(4):
            nx = x + self.dx[d]
            ny = y + self.dy[d]
            if nx >= 0 and nx < self.K and ny >= 0 and ny < self.K:
                dic[d] = abs(self.blocks[nx][ny] - nx * self.K - ny - 1)
            else:
                dic[d] = -1
        
        dic = dict(sorted(dic.items(),key=lambda x:x[1],reverse=True)) # 按块实际位置与应该所在位置的距离排序，优先处理大的
        # print(dic.keys())
        # 四个方向移动
        for d in dic.keys():
            nx = x + self.dx[d]
            ny = y + self.dy[d]
            # if step == 0 and d == 2:
            #     print(step, line, x, y, nx, ny)
            # print(dic.keys())
            # print('===========')
            # os.system('pause')
            if nx <= line:
                continue
            if nx >= 0 and nx < self.K and ny >= 0 and ny < self.K:
                path.append(d)
                self.blocks[x][y] = self.blocks[nx][ny]
                self.blocks[nx][ny] = 0
                val = self.hash()
                # if val == 80533122198148894:
                #     print('step = ', step)
                #     print(self.blocks)

                if (val not in self.mp) or (step + 1 < self.mp[val]): # 判断移动后的图是否已经存在
                    # if step == 0 and d == 2:
                    #     print(step, line, x, y, nx, ny)
                    #     print('tag3')
                    # self.mp[val] = step + 1
                    # if val == 80533122198148894:
                    #     print('--------------------')
                    #     print('|         %d       |', self.mp[val])
                    #     print('------------------- ')
                    self.mp[val] = step + 1
                    self.Dfs(nx, ny, step + 1, path)
                self.blocks[nx][ny] = self.blocks[x][y]
                self.blocks[x][y] = 0
                path.pop()
                
