import requests

class Notification:
    def send_lotto_buying_message(self, body: dict, webhook_url: str) -> None:
        assert type(webhook_url) == str

        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 :moneybag: 잔액: {body['balance']}\n```{lotto_number_str}```"
        self._send_discord_webhook(webhook_url, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]

        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]

        # lotto_number to string
        lotto_number = '\n'.join(x for x in lotto_number)

        return lotto_number

    def send_win720_buying_message(self, body: dict, webhook_url: str) -> None:
        assert type(webhook_url) == str

        if body.get("resultCode") != "100":
            return

        win720_round = body.get("round", "?")
        if win720_round == "?":
            try:
                win720_round = body.get("saleTicket", "").split("|")[-2]
            except:
                win720_round = "?"

        if not body.get("saleTicket"):
            win720_number_str = "번호 정보 없음"
        else:
            win720_number_str = self.make_win720_number_message(body.get("saleTicket"))

        message = f"{win720_round}회 연금복권 구매 :moneybag: 잔액: {body['balance']}\n```{win720_number_str}```"
        self._send_discord_webhook(webhook_url, message)

    def make_win720_number_message(self, win720_number: str) -> str:
        formatted_numbers = []
        for number in win720_number.split(","):
            formatted_number = f"{number[0]}조 " + " ".join(number[1:])
            formatted_numbers.append(formatted_number)
        return "\n".join(formatted_numbers)

    def send_lotto_winning_message(self, winning: dict, webhook_url: str) -> None:
        assert type(winning) == dict
        assert type(webhook_url) == str

        try:
            round = winning["round"]
            money = winning["money"]

            if winning["money"] != "0":
                message = f"로또 __***{winning['round']}회***__ - __***{winning['money']}원***__ 당첨 :tada:"
            else:
                message = ":money_with_wings: 당첨 내역이 없습니다."

            self._send_discord_webhook(webhook_url, message)
        except KeyError:
            message = ":money_with_wings: 당첨 내역이 없습니다."
            self._send_discord_webhook(webhook_url, message)

    def send_win720_winning_message(self, winning: dict, webhook_url: str) -> None:
        assert type(winning) == dict
        assert type(webhook_url) == str

        try:
            round = winning["round"]
            money = winning["money"]

            if winning["money"] != "-":
                message = f"연금복권 __***{winning['round']}회***__ - __***{winning['money']}원***__ 당첨 :tada:"

            self._send_discord_webhook(webhook_url, message)
        except KeyError:
            pass

    def _send_discord_webhook(self, webhook_url: str, message: str) -> None:
        payload = {"content": message}
        requests.post(webhook_url, json=payload)
