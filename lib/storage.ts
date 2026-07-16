import path from "path";
import { mkdir, writeFile } from "fs/promises";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const r2AccountId = process.env.R2_ACCOUNT_ID;
const r2AccessKeyId = process.env.R2_ACCESS_KEY_ID;
const r2SecretAccessKey = process.env.R2_SECRET_ACCESS_KEY;
const r2Bucket = process.env.R2_BUCKET;
const r2PublicBaseUrl = process.env.R2_PUBLIC_BASE_URL;
const r2Endpoint = r2AccountId ? `https://${r2AccountId}.r2.cloudflarestorage.com` : undefined;

const hasR2 = Boolean(r2AccountId && r2AccessKeyId && r2SecretAccessKey && r2Bucket);

const r2Client = hasR2
  ? new S3Client({
      region: "auto",
      endpoint: r2Endpoint,
      credentials: {
        accessKeyId: r2AccessKeyId!,
        secretAccessKey: r2SecretAccessKey!,
      },
    })
  : null;

async function saveLocally(file: File, folder: 'modules' | 'welcome') {
  const bytes = Buffer.from(await file.arrayBuffer());
  const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_');
  const dir = path.join(process.cwd(), 'public', 'uploads', folder);
  await mkdir(dir, { recursive: true });
  const fileName = `${Date.now()}-${safeName}`;
  const fullPath = path.join(dir, fileName);
  await writeFile(fullPath, bytes);
  return `/uploads/${folder}/${fileName}`;
}

export async function saveUploadedVideo(file: File, folder: 'modules' | 'welcome') {
  if (!r2Client) {
    return saveLocally(file, folder);
  }

  const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_');
  const key = `${folder}/${Date.now()}-${safeName}`;
  const body = Buffer.from(await file.arrayBuffer());

  await r2Client.send(
    new PutObjectCommand({
      Bucket: r2Bucket!,
      Key: key,
      Body: body,
      ContentType: file.type || 'application/octet-stream',
    }),
  );

  if (r2PublicBaseUrl) {
    return `${r2PublicBaseUrl.replace(/\/$/, '')}/${key}`;
  }

  return `${r2Endpoint?.replace(/\/$/, '')}/${r2Bucket}/${key}`;
}
