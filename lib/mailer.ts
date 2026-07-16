import nodemailer from "nodemailer";

const smtpHost = process.env.SMTP_HOST || "smtp.office365.com";
const smtpPort = Number(process.env.SMTP_PORT || "587");
const smtpUser = process.env.SMTP_USER || "epowell@cflinc.org";
const smtpPass = process.env.SMTP_PASS || "";
const smtpFrom = process.env.SMTP_FROM || "epowell@cflinc.org";
const mailEnabled = Boolean(smtpPass);

const transporter = nodemailer.createTransport({
  host: smtpHost,
  port: smtpPort,
  secure: smtpPort === 465,
  auth: smtpPass ? { user: smtpUser, pass: smtpPass } : undefined,
});

export async function sendInviteEmail(email: string, name: string, inviteUrl: string) {
  const subject = "Your Center of Family Love training account";
  const text = [
    `Hi ${name},`,
    "",
    "You've been invited to the Center of Family Love training portal.",
    `Set up your account here: ${inviteUrl}`,
    "",
    "If you weren't expecting this email, please ignore it.",
  ].join("\n");

  if (!mailEnabled) {
    console.log(`[invite-email:dry-run] from=${smtpFrom} to=${email} subject=${subject} url=${inviteUrl}`);
    return;
  }

  await transporter.sendMail({
    from: smtpFrom,
    to: email,
    subject,
    text,
  });
}
