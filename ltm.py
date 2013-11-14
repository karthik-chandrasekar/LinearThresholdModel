import networkx as nx
import logging, os

class ltm:

    def __init__(self):
            
        self.dir_name = "input"
        self.file_name = "amazon0302.txt"
        self.logger_file = "ltm.log"
        self.edge_to_weight_dict = {}
        self.node_to_incoming_edge_dict = {}
        self.node_to_activation_count_dict = {}    

    def run_main(self):
        self.initialize_logger()
        self.open_file()
        self.load_graph()
        self.close_file()
        self.pre_processing()
        self.run()
    
    def initialize_logger(self):
        logging.basicConfig(filename=self.logger_file, level=logging.INFO)
        logging.info("Initialized logger") 

    def open_file(self):
        self.fd = open(os.path.join(self.dir_name, self.file_name), 'rb')

    def load_graph(self):
        self.G  = nx.read_edgelist(self.fd, create_using=nx.DiGraph())
        self.nodes_list = self.G.nodes()
 
    def close_file(self):
        self.fd.close()


    def pre_processing(self):   
        for node in self.nodes_list:
            neighbors_list = self.G.neighbors(node)
            if len(neighbors_list) == 0:
                continue
            edge_weight = 1/float(len(neighbors_list))
            for neighbor in neighbors_list:
                edge_name = node+"TO"+neighbor
                self.edge_to_weight_dict[edge_name] = edge_weight
                self.node_to_incoming_edge_dict.setdefault(neighbor, []).append(edge_name)        
        import pdb;pdb.set_trace()

    def run(self):
        for node in self.nodes_list:
            if not node:
                continue
            count = self.find_activation_count(node) 
            self.node_to_activation_count_dict[node] = count 

    def find_activation_count(self, node):
        pass               


if __name__ == "__main__":
    ltm_obj = ltm()
    ltm_obj.run_main()
