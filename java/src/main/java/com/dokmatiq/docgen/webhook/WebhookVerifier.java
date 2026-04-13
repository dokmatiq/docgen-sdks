package com.dokmatiq.docgen.webhook;

import com.dokmatiq.docgen.exception.DocGenException;
import com.dokmatiq.docgen.internal.JsonMapper;
import com.dokmatiq.docgen.model.WebhookPayload;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Webhook signature verification utility.
 *
 * <pre>{@code
 * WebhookPayload payload = WebhookVerifier.verify(requestBody, signatureHeader, secret);
 * System.out.println("Job " + payload.jobId() + " status: " + payload.status());
 * }</pre>
 */
public final class WebhookVerifier {
    private WebhookVerifier() {}

    /**
     * Verify a DocGen webhook signature and parse the payload.
     *
     * @param body      Raw request body.
     * @param signature Value of the X-DocGen-Signature header.
     * @param secret    The callback_secret used when creating the job.
     * @return Parsed webhook payload.
     * @throws DocGenException if the signature is invalid.
     */
    public static WebhookPayload verify(String body, String signature, String secret) {
        return verify(body.getBytes(StandardCharsets.UTF_8), signature, secret);
    }

    /**
     * Verify a DocGen webhook signature and parse the payload.
     *
     * @param body      Raw request body bytes.
     * @param signature Value of the X-DocGen-Signature header.
     * @param secret    The callback_secret used when creating the job.
     * @return Parsed webhook payload.
     * @throws DocGenException if the signature is invalid.
     */
    public static WebhookPayload verify(byte[] body, String signature, String secret) {
        try {
            var mac = Mac.getInstance("HmacSHA256");
            mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
            var expected = bytesToHex(mac.doFinal(body));

            if (!MessageDigest.isEqual(
                    expected.getBytes(StandardCharsets.UTF_8),
                    signature.getBytes(StandardCharsets.UTF_8))) {
                throw new DocGenException("Invalid webhook signature");
            }

            return JsonMapper.fromJson(body, WebhookPayload.class);
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            throw new DocGenException("HMAC computation failed", e);
        }
    }

    private static String bytesToHex(byte[] bytes) {
        var sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
