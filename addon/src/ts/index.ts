const binding = require('node-gyp-build')(__dirname + '../../../');
const generateProof = binding.generateProof;

export const CIRCUITS = {
  JOINSPLIT_1X2: 12,
  JOINSPLIT_1X3: 13,
  JOINSPLIT_2X2: 22,
  JOINSPLIT_2X3: 23,
  JOINSPLIT_8X2: 82,
};

export type Proof = {
  pi_a: string[];
  pi_b: string[][];
  pi_c: string[];
};

export type FormattedJsonInputs = {
  merkleRoot: string;
  boundParamsHash: string;
  nullifiers: string[];
  commitmentsOut: string[];
  token: string;
  publicKey: string[];
  signature: string[];
  randomIn: string[];
  valueIn: string[];
  pathElements: string[];
  leavesIndices: string[];
  nullifyingKey: string;
  npkOut: string[];
  valueOut: string[];
};

export type NativeProofProgressCallback = (progress: number) => void;

export const nativeProve = (
  circuitId: number,
  datBuffer: Buffer,
  zkeyBuffer: Buffer,
  inputJson: FormattedJsonInputs,
  progressCallback: NativeProofProgressCallback,
): Proof => {
  const proofString = generateProof(
    circuitId,
    datBuffer,
    zkeyBuffer,
    JSON.stringify(inputJson),
    progressCallback,
  );
  return JSON.parse(proofString);
};
