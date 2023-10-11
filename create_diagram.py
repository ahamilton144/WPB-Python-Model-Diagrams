##### Section 1
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom


##### Section 2
### filename for output png file
filename='diagrams/Pywr-DRB_model_diagram'

### location of icons, downloaded from https://thenounproject.com/
### Note: file paths need to be relative to filename above (e.g., use '../' to back out of diagrams/ directory)
reservoir_icon = '../icons/reservoir.png'
river_icon = '../icons/river.png'
gage_icon = '../icons/measurement.png'
diversion_icon = '../icons/demand.png'


##### Section 3
### customize graphviz attributes
graph_attr = {
    'fontsize': '40',
    'splines': 'spline',
}

##### Section 4
### create a diagram to depict the node network
with Diagram("", filename=filename, show=False, graph_attr=graph_attr, direction='LR'):

    ##### Section 5
    ### diversion nodes
    graph_attr['bgcolor'] = 'mediumseagreen'

    with Cluster('NYC Diversion', graph_attr=graph_attr):
        NYCDiversion = Custom('', diversion_icon)

    with Cluster('NJ Diversion', graph_attr=graph_attr):
        NJDiversion = Custom('', diversion_icon)


    ##### Section 6
    ### function for creating edge with linestyle based on time delay between nodes (days)
    def create_edge(lag_days):
        penwidth = '4'
        if lag_days == 0:
            return Edge(color='black', style='solid', penwidth=penwidth)
        elif lag_days == 1:
            return Edge(color='black', style='dashed', penwidth=penwidth)
        elif lag_days == 2:
            return Edge(color='black', style='dotted', penwidth=penwidth)


    ##### Section 7
    ### cluster of minor nodes within major node
    def create_node_cluster(label, has_reservoir, has_gage):
        if has_reservoir and label in ['Cannonsville', 'Pepacton', 'Neversink']:
            bgcolor='firebrick'
        elif has_reservoir:
            bgcolor='lightcoral'
        else:
            bgcolor='cornflowerblue'
        graph_attr['bgcolor'] = bgcolor

        with Cluster(label, graph_attr=graph_attr):
            cluster_river = Custom('', river_icon)

            if has_reservoir:
                cluster_reservoir = Custom('', reservoir_icon)
                cluster_river >> create_edge(0) >> cluster_reservoir
                if has_gage:
                    cluster_gage = Custom('', gage_icon)
                    cluster_reservoir >> create_edge(0) >> cluster_gage
                    return {'river': cluster_river, 'reservoir': cluster_reservoir, 'out': cluster_gage}
                else:
                    return {'river': cluster_river, 'reservoir': cluster_reservoir, 'out': cluster_reservoir}
            else:
                if has_gage:
                    cluster_gage = Custom('', gage_icon)
                    cluster_river >> create_edge(0) >> cluster_gage
                    return {'river': cluster_river, 'reservoir': None, 'out': cluster_gage}
                else:
                    return {'river': cluster_river, 'reservoir': None, 'out': cluster_river}


    ##### Section 8
    ### river nodes
    Lordville = create_node_cluster('Lordville', has_reservoir=False, has_gage=True)
    Montague = create_node_cluster('Montague', has_reservoir=False, has_gage=True)
    Trenton1 = create_node_cluster('Trenton 1', has_reservoir=False, has_gage=False)
    Trenton2  = create_node_cluster('Trenton 2', has_reservoir=False, has_gage=True)
    DelawareBay  = create_node_cluster('Delaware Bay', has_reservoir=False, has_gage=True)

    ### reservoir nodes
    Cannonsville = create_node_cluster('Cannonsville', has_reservoir=True, has_gage=True)
    Pepacton = create_node_cluster('Pepacton', has_reservoir=True, has_gage=True)
    Neversink = create_node_cluster('Neversink', has_reservoir=True, has_gage=True)
    Prompton = create_node_cluster('Prompton', has_reservoir=True, has_gage=False)
    Wallenpaupack = create_node_cluster('Wallenpaupack', has_reservoir=True, has_gage=False)
    ShoholaMarsh = create_node_cluster('Shohola Marsh', has_reservoir=True, has_gage=True)
    Mongaup = create_node_cluster('Mongaup', has_reservoir=True, has_gage=True)
    Beltzville = create_node_cluster('Beltzville', has_reservoir=True, has_gage=True)
    FEWalter = create_node_cluster('F.E. Walter', has_reservoir=True, has_gage=True)
    MerrillCreek = create_node_cluster('Merrill Creek', has_reservoir=True, has_gage=False)
    Hopatcong = create_node_cluster('Hopatcong', has_reservoir=True, has_gage=False)
    Nockamixon = create_node_cluster('Nockamixon', has_reservoir=True, has_gage=False)
    Assunpink = create_node_cluster('Assunpink', has_reservoir=True, has_gage=True)
    StillCreek = create_node_cluster('Still Creek', has_reservoir=True, has_gage=False)
    Ontelaunee = create_node_cluster('Ontelaunee', has_reservoir=True, has_gage=False)
    BlueMarsh = create_node_cluster('Blue Marsh', has_reservoir=True, has_gage=True)
    GreenLane = create_node_cluster('Green Lane', has_reservoir=True, has_gage=False)


    ##### Section 9
    ### tie them all together, with edge linestyles designating time delay between nodes.
    Cannonsville['reservoir'] >> create_edge(0) >> NYCDiversion
    Pepacton['reservoir'] >> create_edge(0) >> NYCDiversion
    Neversink['reservoir'] >> create_edge(0) >> NYCDiversion
    Cannonsville['out'] >> create_edge(0) >> Lordville['river']
    Pepacton['out'] >> create_edge(0) >> Lordville['river']
    Lordville['out'] >> create_edge(2) >> Montague['river']
    Neversink['out'] >> create_edge(1) >> Montague['river']
    Prompton['out'] >> create_edge(1) >> Montague['river']
    Wallenpaupack['out'] >> create_edge(1) >> Montague['river']
    ShoholaMarsh['out'] >> create_edge(1) >> Montague['river']
    Mongaup['out'] >> create_edge(0) >> Montague['river']
    Montague['out'] >> create_edge(2) >> Trenton1['river']
    Beltzville['out'] >> create_edge(2) >> Trenton1['river']
    FEWalter['out'] >> create_edge(2) >> Trenton1['river']
    MerrillCreek['out'] >> create_edge(1) >> Trenton1['river']
    Hopatcong['out'] >> create_edge(1) >> Trenton1['river']
    Nockamixon['out'] >> create_edge(0) >> Trenton1['river']
    Trenton1['out'] >> create_edge(0) >> Trenton2['river']
    Trenton1['out'] >> create_edge(0) >> NJDiversion
    Trenton2['out'] >> create_edge(0) >> DelawareBay['river']
    Assunpink['out'] >> create_edge(0) >> DelawareBay['river']
    Ontelaunee['out'] >> create_edge(2) >> DelawareBay['river']
    StillCreek['out'] >> create_edge(2) >> DelawareBay['river']
    BlueMarsh['out'] >> create_edge(2) >> DelawareBay['river']
    GreenLane['out'] >> create_edge(1) >> DelawareBay['river']


