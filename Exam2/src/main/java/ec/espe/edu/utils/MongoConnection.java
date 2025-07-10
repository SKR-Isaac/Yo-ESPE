
package ec.espe.edu.utils;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;

/**
 *
 * @author Isaac Maisincho Crafters_Market DCCO ESPE
 */
public class MongoConnection {
     private static final String URI = "mongodb+srv://isaac:isaac@cluster0.xaitfht.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
    private static final String DATABASE_NAME = "Soccer";
    
    private static MongoClient mongoClient = null;

    private MongoConnection() {
      
    }

    public static MongoDatabase getDatabase() {
        if (mongoClient == null) {
            mongoClient = MongoClients.create(URI);
        }
        return mongoClient.getDatabase(DATABASE_NAME);
    }

    public static void closeConnection() {
        if (mongoClient != null) {
            mongoClient.close();
            mongoClient = null;
        }
    }
    
    }