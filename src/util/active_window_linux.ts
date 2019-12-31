import * as child from 'child_process';

const xpropIdCommand = "xprop -root 32x '\\t$0' _NET_ACTIVE_WINDOW | cut -f 2";
const xpropNamePropCommand = `xprop -id $(${xpropIdCommand}) WM_NAME`;


export default function getActiveWindow(): string {
    const returnString = child.execSync(xpropNamePropCommand).toString();
    const row = returnString.split("=");
    const namePart = row.pop();
    if (namePart != undefined) {
        return JSON.parse(namePart);
    } else {
        throw new Error(`Could not find name from ${returnString}`);
    }
}
