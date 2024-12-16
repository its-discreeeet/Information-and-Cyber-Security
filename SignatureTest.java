package dsa;
import java.security.*;
/*import java.util.Scanner;*/

public class SignatureTest {
    public static void main(String[] args) {

        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
            SecureRandom secrand = new SecureRandom();
            keyGen.initialize(512, secrand);
            
            KeyPair keys1 = keyGen.generateKeyPair();
            PublicKey pubkey1 = keys1.getPublic();
            PrivateKey privkey1 = keys1.getPrivate();
            
            KeyPair keys2 = keyGen.generateKeyPair();
            PublicKey pubkey2 = keys2.getPublic();  
            PrivateKey privkey2 = keys2.getPrivate();

            Signature signalg = Signature.getInstance("DSA");
            signalg.initSign(privkey1);
            String message = "I want my 20000 back asap";
            signalg.update(message.getBytes());

            byte[] signature = signalg.sign();

            Signature verifyalg = Signature.getInstance("DSA");
            verifyalg.initVerify(pubkey1);
            verifyalg.update(message.getBytes());

            if(!verifyalg.verify(signature)){
                System.out.println("Signature does not match!");
            } else {
                System.out.println("Signature matches!");
            }


        } catch(Exception e){
            System.out.println("Error: " + e);
            
        }   
        
    }
}