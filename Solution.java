import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {
	
    List<Wombat> wombats;
	Graph graph;
	Set<Wombat> solution;
	
	public Solution(){
		this.graph = new Graph();
		this.wombats = new ArrayList<Wombat>();
		this.solution = new HashSet<Wombat>();
	}
	
	public Double solution(){
		this.readInput();
		this.getGraph().pushFromSource();
		
		List<Wombat> tempWombats = new ArrayList<Wombat>();
		tempWombats.addAll(this.wombats);
		int cur_index = 0;
		
		while (cur_index < tempWombats.size()){
			cur_index = iterate(cur_index,tempWombats);
		}
		
		this.retrieveOrder(this.getGraph().getSource());
		return this.sumSolution();
		
	}
	
	public Solution(List<Wombat> wombats,Graph g){
		this.graph = g;
		this.wombats = wombats;
	}
	
	public Graph getGraph(){
		return this.graph;
	}
	
	public Collection<Wombat> getWombats(){
		return this.wombats;
	}
	
	public enum NodeType {SOURCE,SINK,NORMAL}
	
	public class Wombat {
		NodeType nodeType;
		Integer id;
		Double value;
		Integer level;
		Integer row;
		Integer index;
		
		Double stored;
		Integer visited;
		Integer current_h;
		
		public Wombat(NodeType ntype,Integer id,Double value,Integer level,Integer row,Integer index){
			this.nodeType = ntype;
			this.value = value;
			this.level = level;
			this.row = row;
			this.index = index;
			this.id = id;
			this.stored = (double) 0;
			this.visited = 0;
			this.current_h = 0;
		}
		
		public String getLocation(){
			switch (this.nodeType){
			case NORMAL:
				return String.format("%d.%d.%d", level,row,index);
			case SINK:
				return "SINK";
			case SOURCE:
				return "SOURCE";
			}
			return null;
		}
		
		public String printValue(){
			switch (this.nodeType){
			case NORMAL:
				return String.format("%.2f", this.getValue());
			case SINK:
				return "SINK";
			case SOURCE:
				return "SOURCE";
			}
			return null;
		}
		
		public Double getValue(){
			return this.value;
		}
		
		public String[] getRequired(){
			String[] requireParents = new String[3];
			requireParents[0] = String.format("%d.%d.%d",this.level-1,this.row,this.index);
			requireParents[1] = String.format("%d.%d.%d",this.level-1,this.row-1,this.index);
			requireParents[2] = String.format("%d.%d.%d",this.level-1,this.row,this.index-1);
			return requireParents;
		}
		
		public Double getStored(){
			return this.stored;
		}
		
		public Integer getCurHeight(){
			return this.current_h;
		}
		
		public void setCurHeight(Integer h){
			this.current_h = h;
		}
		
		public void setStored(Double stored){
			this.stored = stored;
		}
		
		public void setVisited(Integer visited){
			this.visited = visited;
		}
		
		public Integer getVisited(){
			return this.visited;
		}
	}
	
	public class Capacitance {
		
		Double capacity;
		Double flow;
		
		public Capacitance(){
			this.capacity = (double) 0;
			this.flow = (double) 0;
		}
		
		public Capacitance(Double capacity){
			this.capacity = capacity;
			this.flow = (double) 0 ;
		}
		
		public void setFlow(Double flow){
			this.flow = flow;
		}
		
		public Double getResidual(){
			return this.capacity - this.flow;
		}
		
		public Double getFlow(){
			return this.flow;
		}
		
		public String toString(){
			return String.format("%.2f/%.2f", this.flow,this.capacity);
		}
	}
	
	public class Graph {
		
		HashMap<Wombat,HashMap<Wombat,Capacitance>> graph;
		Wombat source;
		Wombat sink;
		
		public Graph(){
			this.graph = new HashMap<Wombat,HashMap<Wombat,Capacitance>>();
		}
		
		public boolean exist(Wombat origin,Wombat dest){
			if (graph.containsKey(origin)){
				return graph.get(origin).containsKey(dest);
			}
			return false;
		}
		
		public int getSize(){
			return this.graph.size();
		}
		
		public Wombat getSource(){
			return this.source;
		}
		
		public Wombat getSink(){
			return this.sink;
		}
		
		public void printCapacity(boolean seeAll){
	        for (Wombat origin:graph.keySet()){
	        	HashMap<Wombat,Capacitance> row = graph.get(origin);
	        	for (Wombat dest:row.keySet()){
	        		Capacitance capacity = row.get(dest);
	        		if (!seeAll){
	        			if (capacity.getResidual() == 0 && capacity.getFlow() == 0){
	        				continue;
	        			}
	        		}
	        		
	        		String s = String.format("%s to %s: %s", origin.printValue(),dest.printValue(),capacity.toString());
	        		System.out.println(s);
	        	}
	        }
		}
		
		public void addNode(Wombat w){
			switch (w.nodeType){
			case SINK:
				this.sink = w;
				break;
			case SOURCE:
				this.source = w;
				break;
			default:
				break;
			
			}
			this.graph.put(w, new HashMap<Wombat,Capacitance>());
		}
		
		public void pushFlow(Wombat origin,Wombat dest){
			Double sending = Math.min(origin.getStored(),this.getResidual(origin, dest));
			updateResidualGraph(origin,dest,sending);
		}
		
		public void updateResidualGraph(Wombat origin,Wombat dest,Double sending){
			origin.setStored(origin.getStored() - sending);
			dest.setStored(dest.getStored() + sending);
			this.updateCapacitance(origin, dest, sending);
		}
		
		public Double getResidual(Wombat origin,Wombat dest){
			if (this.graph.get(origin).containsKey(dest)){
				return this.graph.get(origin).get(dest).getResidual();
			}
			return (double) 0;
		}
		
		public void updateCapacitance(Wombat origin,Wombat dest,Double sending){
			Capacitance forward = this.graph.get(origin).get(dest);
			forward.setFlow(forward.getFlow() + sending);
			
			Capacitance reverse = this.graph.get(dest).get(origin);
			if (reverse == null){
				reverse = new Capacitance();
				this.graph.get(dest).put(origin, reverse);
			}
			reverse.setFlow(reverse.getFlow() - sending);
		}
		
		public void addEdge(Wombat origin,Wombat dest,Capacitance capacity){
			this.graph.get(origin).put(dest, capacity);
		}
		
		public void pushFromSource(){
			this.source.setStored(Double.POSITIVE_INFINITY);
			this.source.setCurHeight(this.graph.size());
			HashMap<Wombat,Capacitance> src_edges = this.graph.get(this.source);
			for (Wombat neighbor:src_edges.keySet()){
				this.pushFlow(this.source, neighbor);
			}
		}
		
		public Collection<Wombat> getRow(Wombat w){
			return this.graph.get(w).keySet();
		}
	}
	
	public Wombat getWombat(int index){
		// source
		if (index == this.wombats.size()+1){
			return this.getGraph().getSource();
		
		}
		if (index == this.wombats.size()){
			return this.getGraph().getSink();
		}
		if (index >= this.wombats.size()+2){
			return null;
		}
		return this.wombats.get(index);
	}
	
	public void pushToNeighbor(Wombat cur_w,Wombat cur_v){
		
		if (this.getGraph().getResidual(cur_w, cur_v) > 0 && cur_w.getCurHeight() > cur_v.getCurHeight()) {
			this.getGraph().pushFlow(cur_w, cur_v);
		}
		else {
			cur_w.setVisited(cur_w.getVisited() + 1);
		}
	}
	
	public void moveToNextLevel(Wombat cur_w,int n){
		int min_height = Integer.MAX_VALUE;
		for (int i =0;i<n;i++){
			Wombat cur_v = this.getWombat(i);
			if (this.getGraph().getResidual(cur_w, cur_v) > 0){
				min_height = Math.min(min_height, cur_v.getCurHeight());
				cur_w.setCurHeight(min_height+1);
			}
		}
		cur_w.setVisited(0);
	}
	
	public void pushStoredFlow(Wombat cur_w){
		int n = this.getGraph().getSize();
		if (cur_w.getVisited() >= n){
			moveToNextLevel(cur_w,n);
		}
		else {
			int v = cur_w.getVisited();
			
			Wombat cur_v = this.getWombat(v);
			pushToNeighbor(cur_w,cur_v);
		}
	}
	
	public int iterate(int cur_index,List<Wombat> wombat_li){
		Wombat cur_w = wombat_li.get(cur_index);
		Integer n = this.getGraph().getSize();
		
		Integer old_height = cur_w.getCurHeight();
		while (cur_w.getStored() > 0){
			this.pushStoredFlow(cur_w);
		}
		if (cur_w.getCurHeight() > old_height){
			Wombat shifted = wombat_li.remove(cur_index);
			wombat_li.add(0, shifted);
			return cur_index = 0;
		} else {
			return cur_index + 1;
		}
	}
	
	public void printHeights(){
		int index = 0;
		for (Wombat w:this.wombats){
			index+=1;
			System.out.printf("%.2f:%d -> height: %d\n",w.getValue(),index,w.getCurHeight());
		}
		System.out.print(this.getGraph().getSink().getCurHeight()+",");
		System.out.println(this.getGraph().getSource().getCurHeight());
		System.out.println("\n");
	}
	
	public void retrieveOrder(Wombat source){
		for (Wombat dest:this.getGraph().getRow(source)){
			Double r = this.getGraph().getResidual(source, dest);
			if (!this.solution.contains(dest)){
				if (r > 0){
					this.solution.add(dest);
					retrieveOrder(dest);
				}
			}
		}
	}
	
	
	public Double sumSolution(){
		Double sum = (double) 0;
		for (Wombat w:this.solution){
			if (w.nodeType == NodeType.NORMAL){
				sum+=w.value;
			}
		}
		return sum;
	}
	
	public void readInput(){
		
        Scanner stdin = new Scanner(System.in);
        Integer n = Integer.parseInt(stdin.nextLine());
        
        HashMap<String,Wombat> wombats = new HashMap<String,Wombat>();
        Graph adjacency = this.getGraph();
        Integer id_counter = 0;
        for(int level = 0; level< n;level++){
        	for (int row = 0;row <= level;row++){
        		if (stdin.hasNextLine()){
        			String str_row = stdin.nextLine();
        			String[] entries = str_row.split(" ");
        			for (int index = 0;index < entries.length;index++){
        				id_counter+=1;
        				Double val = Double.parseDouble(entries[index]);
        				Wombat w = new Wombat(NodeType.NORMAL,id_counter,val,level,row,index);
        				wombats.put(w.getLocation(), w);
        				this.wombats.add(w);
        				adjacency.addNode(w);
        				
        				for (String required: w.getRequired()){
        					if (wombats.containsKey(required)){
        						Wombat requiredW = wombats.get(required);
        						Capacitance c = new Capacitance(Double.POSITIVE_INFINITY);
        						adjacency.addEdge(w,requiredW, c);
        					}
        				}
        			}
        		}
        	}
        }
        
        Wombat source = new Wombat(NodeType.SOURCE,++id_counter,null,null,null,null);
        Wombat sink = new Wombat(NodeType.SINK,++id_counter,null,null,null,null);
        adjacency.addNode(source);
        adjacency.addNode(sink);
        for (Wombat w:wombats.values()){
        	Capacitance c = new Capacitance(Math.abs(w.getValue()));
        	if (w.value > 0){
        		adjacency.addEdge(source,w, c);
        	} else if (w.value < 0){
        		adjacency.addEdge(w,sink, c);
        	}
        }
        
        for (Wombat origin:this.getGraph().graph.keySet()){
        	for (Wombat dest:this.getGraph().graph.keySet()){
        		if (origin == dest){
        			continue;
        		}
        		if (!adjacency.exist(origin,dest)){
        			adjacency.addEdge(origin, dest, new Capacitance());
        		}
        	}
        }
	}

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
    	Solution s = new Solution();
    	Integer cuteVal = s.solution().intValue();
    	System.out.println(cuteVal);
    	
    }
}
