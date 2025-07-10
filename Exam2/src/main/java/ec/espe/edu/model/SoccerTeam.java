
package ec.espe.edu.model;

/**
 *
 * @author Isaac Maisincho Crafters_Market DCCO ESPE
 */
public class SoccerTeam {
    
    private int id;
    private String name;
    private float ExpensiveTeam;
    private String MostExpensiveSigning;
    private float TranferPrice;

    public SoccerTeam(int id, String name, float ExpensiveTeam, String MostExpensiveSigning, float TranferPrice) {
        this.id = id;
        this.name = name;
        this.ExpensiveTeam = ExpensiveTeam;
        this.MostExpensiveSigning = MostExpensiveSigning;
        this.TranferPrice = TranferPrice;
    }

    /**
     * @return the id
     */
    public int getId() {
        return id;
    }

    /**
     * @param id the id to set
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * @return the name
     */
    public String getName() {
        return name;
    }

    /**
     * @param name the name to set
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * @return the ExpensiveTeam
     */
    public float getExpensiveTeam() {
        return ExpensiveTeam;
    }

    /**
     * @param ExpensiveTeam the ExpensiveTeam to set
     */
    public void setExpensiveTeam(float ExpensiveTeam) {
        this.ExpensiveTeam = ExpensiveTeam;
    }

    /**
     * @return the MostExpensiveSigning
     */
    public String getMostExpensiveSigning() {
        return MostExpensiveSigning;
    }

    /**
     * @param MostExpensiveSigning the MostExpensiveSigning to set
     */
    public void setMostExpensiveSigning(String MostExpensiveSigning) {
        this.MostExpensiveSigning = MostExpensiveSigning;
    }

    /**
     * @return the TranferPrice
     */
    public float getTranferPrice() {
        return TranferPrice;
    }

    /**
     * @param TranferPrice the TranferPrice to set
     */
    public void setTranferPrice(float TranferPrice) {
        this.TranferPrice = TranferPrice;
    }
        
    }