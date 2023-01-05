import com.fiserv.fdc.FDConnectUtils;
import com.fiserv.fdc.inquiry.model.FDConnectInquiryRequest;
import com.fiserv.fdc.inquiry.model.FDConnectInquiryResponse;
import com.fiserv.fdc.sale.model.FDConnectSaleRequest;
import com.fiserv.fdc.sale.model.FDConnectSaleResponse;
import com.fiserv.fdc.response.model.FDConnectDecryptRequest;
import com.fiserv.fdc.response.model.FDConnectDecryptResponse;
import com.google.gson.Gson;

public class Test {
        public static void main(String[] args) {
                       
 
        FDConnectSaleRequest request = new FDConnectSaleRequest();
        request.setMerchantId("470000012765500");
        request.setKey("myak+AZNujouXgWnVdbteXqTfGXio3oB8/yHD7mSVKw=");
        request.setIv("3lOcRGUBshREdoV8dhWv5g==");
        request.setApiURL("https://test.fdconnect.com/FirstPayL2Services/getToken");
        request.setAmount("1");
        request.setCurrencyCode("INR");
        request.setMerchantTxnId("TRA12ff3f456");
        request.setTransactionType("sale");        
        request.setResultURL("http://localhost:8080");
        request.setUdf1("EDU-STU-2022-00002");
        request.setUdf2("ADVIKA PATI");
        request.setUdf3("2110102");
        request.setUdf4("SamsPortalId");  


        FDConnectSaleResponse resp = FDConnectUtils.saleTxn(request);
        System.out.println("resp SessionTokenId :" + resp.getSessionTokenId());
        System.out.println("respErrorCode :"+resp.getErrorCode());
        System.out.println("ErrorMessage :"+resp.getErrorMessage());               
        

                // FDConnectSaleRequest request = new FDConnectSaleRequest("470000087081990",
                // "5gzhd8sBVDdJyLpn3hEXNyrQNm6qh7fUlPTIz9EhKbk=","VdA4m1prGGFGFLjSDyKEMw==",
                // "https://www.fdconnect.com/FDConnectL3Services/getToken",
                // "10","INR","refrdtefdfd5435","sale",
                // "http://localhost:8080");
                // FDConnectSaleResponse resp = FDConnectUtils.saleTxn(request);
                // System.out.println("resp SessionTokenId :" + resp.getSessionTokenId());
                // System.out.println("respErrorCode :"+resp.getErrorCode());
                // System.out.println("ErrorMessage :"+resp.getErrorMessage()); 
                

                //  FDConnectSaleRequest request = new FDConnectSaleRequest("470000012765500",
                // "myak+AZNujouXgWnVdbteXqTfGXio3oB8/yHD7mSVKw=","3lOcRGUBshREdoV8dhWv5g==",
                // " https://test.fdconnect.com/FirstPayL2Services/getToken",
                // "10","INR","54354retfdsvdcvcx","sale",
                // "http://localhost:8080");
                // FDConnectSaleResponse resp = FDConnectUtils.saleTxn(request);
                // System.out.println("resp SessionTokenId :" + resp.getSessionTokenId());
                // System.out.println("respErrorCode :"+resp.getErrorCode());
                // System.out.println("ErrorMessage :"+resp.getErrorMessage());



   

        //     FDConnectInquiryRequest firstPayInquiryRequest =
        //             new  FDConnectInquiryRequest("470000012765500",
        //                     "myak+AZNujouXgWnVdbteXqTfGXio3oB8/yHD7mSVKw=",
        //                     "3lOcRGUBshREdoV8dhWv5g==",
        //                     "https://test.fdconnect.com/FirstPayL2Services/getTxnInquiryDetail",
        //                     "ICP000011",
        //                     "");
        //     FDConnectInquiryResponse resp = FDConnectUtils.inquiryTxn(firstPayInquiryRequest);
        //     String inquiryStatus= new Gson().toJson(resp);
        //     System.out.println(inquiryStatus);
         


        //   FDConnectDecryptRequest fdConnectDecryptRequest = new FDConnectDecryptRequest("470000012765500",
        //                 "h2sUPU86ytjDciY1EEAPcahsPhbyUzQOJq3A6p7qVItNoHrXM5FH3uZwoRIGizlduFAmGk+3vuNJPgGu90IfTvEVT992NZnjm7xLGwE+lmgj6otzIh2nefXAGVHPA70wZk8tsTd2cYmOENUy+9ackijJ2AQhf1yWTZLuiKLmAjMq5zXqx0FWKloXtR9N1EhT5vCOeQ4vOAdmA89lTRu0jm57MlwrEdx9jxQWmN5k/1X+KB+5FyL4vx4dIiYeDGL/r0119BEI2EDTEfCPD1dPSBfOGfEr4WfFC+6KxBObzi8gBEUkc8Lp/8NJUiR9imO5",
        //         "2022080959113800","https://test.fdconnect.com/FirstPayL2Services/decryptMerchantResponse");

        // FDConnectDecryptResponse resp = FDConnectUtils.decryptMsg(fdConnectDecryptRequest);
        // //   System.out.println(FDConnectUtils.decryptMsg(fdConnectDecryptRequest));
        // //   System.out.println(new Gson().toJson(resp));
        //   String dR=new Gson().toJson(resp);
        //   System.out.println("Response-->"+dR);


        
          
        }
}



