import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.ThreadLocalRandom;

public class Maze {
    private static String[][] maze = new String[20][20];
    private static String[][] maze1 = new String[4][7];
    private static String[][] maze2 = new String[16][16];

    public static void main(String[] args) {


        for (int row = 0; row < 20; row++) {
            for (int col = 0; col < 20; col++) {
                maze[row][col] = " - ";
            }
        }
        maze[0][0] = " A ";
        maze[3][6] = " F ";
        maze[15][15] = " F ";


        do {
            generateWallsAndHoles(maze);
            fillMaze1And2();
        } while (!isPath(maze2, 16, 16) || !isPath(maze1, 4, 7));


        for (int row = 0; row < 4; row++) {
            for (int col = 0; col < 7; col++) {
                System.out.print(maze1[row][col]);
            }
            System.out.println();
        }
        if (isPath(maze1, 4, 7))
            System.out.println("Yes");
        else
            System.out.println("No");

        for (int row = 0; row < 16; row++) {
            for (int col = 0; col < 16; col++) {
                System.out.print(maze2[row][col]);
            }
            System.out.println();
        }

        if (isPath(maze2, 16, 16))
            System.out.println("Yes");
        else
            System.out.println("No");


        for (int row = 0; row < 20; row++) {
            for (int col = 0; col < 20; col++) {
                System.out.print(maze[row][col]);
            }
            System.out.println();
        }

        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < maze.length; i++)//for each row
        {
            for (int j = 0; j < maze.length; j++)//for each column
            {
                builder.append(maze[i][j] + "");//append to the output string
                if (j < maze.length-1)//if this is not the last row element
                    builder.append(" ");//then add comma (if you don't like commas you can use spaces)
            }
            builder.append("\n");//append new line at the end of the row
        }
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("generated_maze.txt"));
            writer.write(builder.toString());//save the string representation of the board
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        /*- --WWW- -
       ---W--- W
       -WW H -- H  -
       ---WW-- -
       ----- H - -;*/

        /*String[][] arr = {{"-", "-", "-", "W", "-", "-", "-", "-"},
                {"-", "-", "-", "W", "-", "-", "-", "-"},
                {"W", "W", "W", "W", "-", "-", "-", "-"},
                {"-", "-", "-", "-", "-", "-", "-", "-"},
                {"-", "-", "-", "-", "-", "-", "-", "-"}};

        if (isPath(arr, 5, 8))
            System.out.println("Yes");
        else
            System.out.println("No");*/

    }

    private static void generateWallsAndHoles(String[][] maze) {
        int wall_count = 0;
        while (wall_count < 60) {
            int rand_row = randomNumber(0, 19);
            int rand_col = randomNumber(0, 19);
            if (checkPossibility(rand_row, rand_col)) {
                maze[rand_row][rand_col] = " W ";
                wall_count++;
            }
        }

        /*int hole_count = 0;
        while (hole_count < 20) {
            int rand_row = randomNumber(0, 19);
            int rand_col = randomNumber(0, 19);
            if (checkPossibility(rand_row, rand_col)) {
                maze[rand_row][rand_col] = " H ";
                hole_count++;
            }
        }
        System.out.println(wall_count + " " + hole_count);*/
    }

    private static void fillMaze1And2() {
        for (int row = 0; row < 4; row++) System.arraycopy(maze[row], 0, maze1[row], 0, 7);

        for (int row = 0; row < 16; row++) System.arraycopy(maze[row], 0, maze2[row], 0, 16);
    }

    private static int randomNumber(int start, int end) {
        return ThreadLocalRandom.current().nextInt(start, end + 1);
    }

    private static boolean checkPossibility(int rand_row, int rand_col) {
        //TODO possible to remove around fruits because isPath return false if no path to fruits found and generate another maze
        return (rand_row != 0 || rand_col != 1) && (rand_row != 1 || rand_col != 0) //around start point
                && (rand_row != 2 || rand_col != 6) && (rand_row != 3 || rand_col != 5) //around fruit 1
                && (rand_row != 3 || rand_col != 7) && (rand_row != 4 || rand_col != 6) //around fruit 1
                && (rand_row != 15 || rand_col != 14) && (rand_row != 15 || rand_col != 16) //around fruit 2
                && (rand_row != 14 || rand_col != 15) && (rand_row != 16 || rand_col != 17) //around fruit 2
                && (rand_row != 0 || rand_col != 0) // agent
                && (rand_row != 3 || rand_col != 6) // fruit 1
                && (rand_row != 15 || rand_col != 15) // fruit 2
                ;
    }

    private static boolean isPath(String[][] matrix, int row, int col) {

        int[][] arr = new int[row][col];

        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                if (matrix[i][j].equals(" W ")/* || matrix[i][j].equals(" H ")*/) {
                    arr[i][j] = -1;
                } else
                    arr[i][j] = 0;
            }
        }
        arr[0][0] = 1;

        for (int i = 1; i < row; i++)
            if (arr[0][i] != -1)
                arr[0][i] = arr[0][i-1];
        for (int j = 1; j < row; j++)
            if (arr[j][0] != -1)
                arr[j][0] = arr[j-1][0];

        for (int i = 1; i < row; i++)
            for (int j = 1; j < col; j++)
                if (arr[i][j] != -1)
                    arr[i][j] = Math.max(arr[i][j-1],
                            arr[i-1][j]);

        return (arr[row-1][col-1] == 1);
    }


    /*private static Graph generateGraph(String[][] matrix, int row, int col) {
        int vectors = 0;
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                if (!matrix[i][j].equals("W") || !matrix[i][j].equals(" H ")) {
                    vectors++;
                }
            }
        }
        System.out.println("vectors: " + vectors);
        Graph g = new Graph(vectors);
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                if (!matrix[i][j].equals("W") || !matrix[i][j].equals(" H ")) {
                    if (i != j) {
                        g.addEdge(i, j);
                        System.out.println("added edge: " + i + " " + j);
                    }
                }
            }
        }

        return g;
    }
*/
}

/*class Graph {
    private int V; // No. of vertices

    // Array  of lists for
    // Adjacency List Representation
    private LinkedList<Integer> adj[];

    // Constructor
    @SuppressWarnings("unchecked")
    Graph(int v) {
        V = v;
        adj = new LinkedList[v];
        for (int i = 0; i < v; ++i)
            adj[i] = new LinkedList();
    }

    // Function to add an edge into the graph
    void addEdge(int v, int w) {
        adj[v].add(w); // AddWto v's list.
    }

    // A function used by DFS
    void DFSUtil(int v, boolean visited[]) {
        // Mark the current node as visited and print it
        visited[v] = true;
        System.out.print(v + " ");

        // Recur for all the vertices adjacent to this
        // vertex
        Iterator<Integer> i = adj[v].listIterator();
        while (i.hasNext()) {
            int n = i.next();
            if (!visited[n])
                DFSUtil(n, visited);
        }
    }

    // The function to do DFS traversal.
    // It uses recursive
    // DFSUtil()
    void DFS(int v) {
        // Mark all the vertices as
        // not visited(set as
        // false by default in java)
        boolean visited[] = new boolean[V];

        // Call the recursive helper
        // function to print DFS
        // traversal
        DFSUtil(v, visited);
    }
}*/

