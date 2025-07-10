
package ec.espe.edu.controller;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import ec.espe.edu.utils.MongoConnection;
import org.bson.Document;

/**
 *
 * @author 
 */
public class SoccerTeamOperation {
    public static void evaluateTransferRisks() {
        MongoDatabase database = MongoConnection.getDatabase();
        MongoCollection<Document> collection = database.getCollection("Teams");

        MongoCursor<Document> cursor = null;
        try {
            cursor = collection.find().iterator();
            while (cursor.hasNext()) {
                Document doc = cursor.next();

                String teamName = doc.getString("name");
                String signing = doc.getString("MostExpensiveSigning");
                float teamValue = doc.getDouble("ExpensiveTeam").floatValue();
                float transfer = doc.getDouble("TransferPrice").floatValue();

                if (teamValue > 0 && transfer > 0.5 * teamValue) {
                    System.out.printf("Riesgo: %s gastó $%.2fM en %s (%.2f%% del valor del equipo)\n",
                            teamName, transfer, signing, (transfer / teamValue) * 100);
                } else {
                    System.out.printf(" Razonable: %s fichó a %s por $%.2fM (%.2f%% del valor del equipo)\n",
                            teamName, signing, transfer, (transfer / teamValue) * 100);
                }
            }
        } finally {
            if (cursor != null) {
                cursor.close();
            }
        }
    }
     }
