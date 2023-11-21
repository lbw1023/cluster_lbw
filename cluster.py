from collections import defaultdict
import typing

class Function(object):
    def __init__(self):
        self.name: str
        self.address: int
        self.module: str
        self.size: int
        self.offset: int
        self.new_address: int
        self.new_offset: int

class Cluster(object):
    def __init__(self):
        self.functions: typing.List[Function]
        self.size: int
        self.address: int
        self.offset: int

cluster_list: typing.List[Cluster]

begin_address: int
end_address: int

# 输入聚簇结果，根据大小和起始地址进行重新分配地址，将聚簇结构体的地址填上
def generate_cluster_address(cluster_list: typing.List[Cluster], begin_address: int):
    current_address = begin_address

    for cluster in cluster_list:
        size = 0
        for function in cluster.functions:
            size += function.size
        cluster.size = size

        # 计算当前地址需要向上取整到 0x1000 的倍数
        remainder = current_address % 0x1000
        if remainder != 0:
            current_address += 0x1000 - remainder

        cluster.address = current_address
        current_address += cluster.size

    return cluster_list

# 函数映射。遍历每个簇的函数，根据函数先后顺序分配空间
def generate_function_address(cluster_list: cluster_list , begin_address: int):
    current_address = begin_address

    for cluster in cluster_list:
        current_address = cluster.address
        for function in cluster.functions:
            function.new_address = current_address
            current_address += function.size

    return cluster_list


class Clustering(object):
    def __init__(self):
        self.llvm_fucntion_name_list: typing.List[str]
        self.llvm_cluster_name_list: typing.List[typing.List[str]]
        self.gcc_function_name_list: typing.List[str]
        self.gcc_function_dic: defaultdict[str , Function]
        self.gcc_cluster_list: typing.List[Cluster]
        self.function_index_cluster: typing.Dict[int, Cluster]

# 得到llvm的结果
    def get_llvm_result(self):
        # 读取聚簇结果
        # 根据簇内函数重合情况进行簇的合并
        visited = set()
        merged_lists: typing.List[typing.List[str]]
        for sublist in lst:
            if sublist in visited:
                continue
            merged_sublist = list(sublist)
            for merged in merged_lists:
                if set(merged) & set(sublist):
                    merged_sublist.extend(merged)
                    visited.add(merged)
            merged_lists.append(merged_sublist)

        # 遍历每个函数，把gcc里面没有的去掉
        for sublist in merged_lists:
            for function_name in sublist:
                if(function_name not in self.gcc_function_name_list):
                    sublist.remove(function_name)
        self.llvm_cluster_name_list = merged_lists

# 将llvm的聚簇结果移植到gcc上
    def llvm_result_convert_to_gcc(self):
        # 找到所有llvm结果里没有，gcc结果有的函数并且进行单独聚簇
        single_function_name_list : typing.List[str]
        llvm_fucntion_name_set : typing.Set[str]
        for name_cluster in self.llvm_cluster_name_list:
            for name in name_cluster:
                llvm_fucntion_name_set.add(name)
        for name in self.gcc_function_name_list:
            if name not in llvm_fucntion_name_set:
                single_function_name_list.append(name)

        # 根据分簇结果进行小的簇的合并
        for cluster in self.llvm_cluster_name_list:
            None

        # 对多出来的函数进行聚簇，放在一个簇里
        cluster_size = 0
        single_functions = []
        for function_name in single_function_name_list:
            target_fucntions = self.gcc_function_dic[function_name]
            for item in target_fucntions:
                cluster_size += item.size
                single_functions.extend(cluster)
        cluster = Cluster()
        cluster.functions = single_functions
        cluster.size = cluster_size
        self.gcc_cluster_list.append(cluster)
        
                 