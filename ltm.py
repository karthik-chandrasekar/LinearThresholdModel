import networkx as nx
import logging, os

class ltm:

    def __init__(self):
            
        self.dir_name = "input"
        self.file_name = "amazon0302.txt"
        self.logger_file = "ltm.log"

        self.NODE_THRESHOLD = 0.5

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

    def run(self):
        for node in self.nodes_list:
            if not node:
                continue
            logging.info("Finding  activation count for %s" % (node))
            self.activated_node_set = set()
            count = self.find_activation_count(node) 
            self.node_to_activation_count_dict[node] = count 

    def find_activation_count(self, node):
        
        activation_count = 0
        neighbors_list = self.G.neighbors(node)
    
        for neighbor in neighbors_list:
            is_activated = self.check_if_activated(neighbor)

            if is_activated and neighbor not in self.activated_node_set:
                self.activated_node_set.add(neighbor)
                activation_count += 1
                neighbors_list.extend(self.G.neighbors(neighbor))        

        return activation_count

     
    def check_if_activated(self, node):

        total_edge_weight = 0

        incoming_edge_list = self.node_to_incoming_edge_dict.get(node)
        if not incoming_edge_list:
            return False

        for edge in incoming_edge_list:
            edge_weight = self.edge_to_weight_dict.get(edge)
            if not edge_weight:
                continue

            total_edge_weight += edge_weight
         
        if total_edge_weight >= self.NODE_THRESHOLD:
            return True

        return False

if __name__ == "__main__":
    ltm_obj = ltm()
    ltm_obj.run_main()
